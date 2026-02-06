"""
File Upload API Routes
Handles file upload, processing, and transaction import
"""
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from database.models import db, Transaction, Category, FileUpload
from services.file_processor import file_processor
from services.data_cleaner import data_cleaner
from ml.categorizer import categorizer

upload_bp = Blueprint('upload', __name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ensure_upload_folder():
    """Ensure upload folder exists"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


@upload_bp.route('', methods=['POST'])
@jwt_required()
def upload_file():
    """
    Upload and process a bank statement file
    
    Accepts: CSV, Excel (.xlsx, .xls), PDF files
    Returns: Processing results with extracted transactions
    """
    try:
        user_id = int(get_jwt_identity())
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Read file content
        file_content = file.read()
        
        # Check file size
        if len(file_content) > MAX_FILE_SIZE:
            return jsonify({
                'error': f'File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB'
            }), 400
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_ext = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        
        # Determine file type
        file_type = file_processor.get_file_type(original_filename)
        
        # Create upload record
        file_upload = FileUpload(
            user_id=user_id,
            filename=unique_filename,
            original_filename=original_filename,
            file_type=file_type,
            file_size=len(file_content),
            status='processing'
        )
        db.session.add(file_upload)
        db.session.commit()
        
        try:
            # Save file (optional - for debugging)
            ensure_upload_folder()
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Process file
            raw_transactions, processing_details = file_processor.process_file(
                file_content, original_filename
            )
            
            if not raw_transactions:
                file_upload.status = 'failed'
                file_upload.error_message = 'No transactions found in file'
                file_upload.processing_details = processing_details
                db.session.commit()
                return jsonify({
                    'error': 'No transactions could be extracted from the file',
                    'details': processing_details
                }), 400
            
            # Clean transactions
            cleaned_transactions = data_cleaner.clean_transactions(raw_transactions)
            cleaning_summary = data_cleaner.get_cleaning_summary(
                raw_transactions, cleaned_transactions
            )
            
            if not cleaned_transactions:
                file_upload.status = 'failed'
                file_upload.error_message = 'No valid transactions after cleaning'
                file_upload.processing_details = {
                    'processing': processing_details,
                    'cleaning': cleaning_summary
                }
                db.session.commit()
                return jsonify({
                    'error': 'No valid transactions after data cleaning',
                    'details': cleaning_summary
                }), 400
            
            # Categorize transactions
            categorized_transactions = []
            for trans in cleaned_transactions:
                # Auto-categorize
                category_name, confidence = categorizer.categorize(
                    trans.get('description'),
                    trans.get('merchant')
                )
                
                # Find category by name
                category = Category.query.filter_by(
                    name=category_name, 
                    is_system=True
                ).first()
                
                categorized_transactions.append({
                    **trans,
                    'suggested_category': category_name,
                    'category_id': category.id if category else None,
                    'category_confidence': round(confidence, 2)
                })
            
            # Update upload record
            file_upload.status = 'completed'
            file_upload.transactions_count = len(categorized_transactions)
            file_upload.processed_at = datetime.utcnow()
            file_upload.processing_details = {
                'processing': processing_details,
                'cleaning': cleaning_summary
            }
            db.session.commit()
            
            return jsonify({
                'message': 'File processed successfully',
                'upload_id': file_upload.id,
                'transactions': categorized_transactions,
                'summary': {
                    **cleaning_summary,
                    'file_type': file_type,
                    'original_filename': original_filename
                }
            }), 200
            
        except Exception as e:
            file_upload.status = 'failed'
            file_upload.error_message = str(e)
            db.session.commit()
            raise
            
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@upload_bp.route('/confirm', methods=['POST'])
@jwt_required()
def confirm_transactions():
    """
    Confirm and save extracted transactions to database
    
    Body: {
        upload_id: int,
        transactions: [
            {
                transaction_date: str,
                type: str,
                amount: float,
                description: str,
                merchant: str,
                category_id: int (optional),
                is_recurring: bool (optional)
            }
        ]
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        upload_id = data.get('upload_id')
        transactions = data.get('transactions', [])
        
        if not transactions:
            return jsonify({'error': 'No transactions to save'}), 400
        
        # Verify upload belongs to user
        if upload_id:
            file_upload = FileUpload.query.filter_by(
                id=upload_id, 
                user_id=user_id
            ).first()
            if not file_upload:
                return jsonify({'error': 'Upload not found'}), 404
        
        # Save transactions
        saved_count = 0
        errors = []
        
        for idx, trans in enumerate(transactions):
            try:
                # Validate required fields
                if not trans.get('amount') or not trans.get('transaction_date'):
                    errors.append(f"Row {idx + 1}: Missing required fields")
                    continue
                
                # Parse date
                trans_date = trans.get('transaction_date')
                if isinstance(trans_date, str):
                    trans_date = datetime.fromisoformat(trans_date.replace('Z', '')).date()
                
                # Create transaction
                transaction = Transaction(
                    user_id=user_id,
                    type=trans.get('type', 'expense'),
                    amount=float(trans['amount']),
                    category_id=trans.get('category_id'),
                    description=trans.get('description', ''),
                    transaction_date=trans_date,
                    merchant=trans.get('merchant', ''),
                    payment_method=trans.get('payment_method', 'bank_transfer'),
                    is_recurring=trans.get('is_recurring', False)
                )
                
                db.session.add(transaction)
                saved_count += 1
                
            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully saved {saved_count} transactions',
            'saved_count': saved_count,
            'errors': errors if errors else None
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@upload_bp.route('/history', methods=['GET'])
@jwt_required()
def get_upload_history():
    """Get user's file upload history"""
    try:
        user_id = int(get_jwt_identity())
        
        uploads = FileUpload.query.filter_by(user_id=user_id)\
            .order_by(FileUpload.created_at.desc())\
            .limit(20)\
            .all()
        
        return jsonify({
            'uploads': [u.to_dict() for u in uploads]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@upload_bp.route('/<int:upload_id>', methods=['DELETE'])
@jwt_required()
def delete_upload(upload_id):
    """Delete an upload record"""
    try:
        user_id = int(get_jwt_identity())
        
        file_upload = FileUpload.query.filter_by(
            id=upload_id, 
            user_id=user_id
        ).first()
        
        if not file_upload:
            return jsonify({'error': 'Upload not found'}), 404
        
        # Delete file if exists
        file_path = os.path.join(UPLOAD_FOLDER, file_upload.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        db.session.delete(file_upload)
        db.session.commit()
        
        return jsonify({'message': 'Upload deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
