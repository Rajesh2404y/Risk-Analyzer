"""
Transaction API Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import db, Transaction, Category
from ml.categorizer import categorizer
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('', methods=['GET'])
@jwt_required()
def get_transactions():
    """Get all transactions for user"""
    try:
        user_id = int(get_jwt_identity())
        
        # Get query parameters
        type_filter = request.args.get('type')
        category_id = request.args.get('category_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 100, type=int)
        
        # Build query
        query = Transaction.query.filter_by(user_id=user_id)
        
        if type_filter:
            query = query.filter_by(type=type_filter)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if start_date:
            query = query.filter(Transaction.transaction_date >= datetime.fromisoformat(start_date).date())
        
        if end_date:
            query = query.filter(Transaction.transaction_date <= datetime.fromisoformat(end_date).date())
        
        transactions = query.order_by(Transaction.transaction_date.desc()).limit(limit).all()
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions],
            'total': len(transactions)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transactions_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction():
    """Create a new transaction"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validation
        if not data.get('amount') or not data.get('type') or not data.get('transaction_date'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Auto-categorize if not provided and type is expense
        category_id = data.get('category_id')
        if not category_id and data['type'] == 'expense':
            try:
                category_name, confidence = categorizer.categorize(
                    data.get('description', ''),
                    data.get('merchant', '')
                )
                # Find category by name
                category = Category.query.filter_by(name=category_name, is_system=True).first()
                if category:
                    category_id = category.id
            except Exception as cat_error:
                print(f"Categorization failed: {cat_error}")
                # Use default category if categorization fails
                default_cat = Category.query.filter_by(name='Others', is_system=True).first()
                if default_cat:
                    category_id = default_cat.id
        
        # Create transaction
        transaction = Transaction(
            user_id=user_id,
            type=data['type'],
            amount=data['amount'],
            category_id=category_id,
            description=data.get('description'),
            transaction_date=datetime.fromisoformat(data['transaction_date']).date(),
            merchant=data.get('merchant'),
            payment_method=data.get('payment_method'),
            is_recurring=data.get('is_recurring', False)
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Error creating transaction: {traceback.format_exc()}")
        return jsonify({'error': f'Failed to create transaction: {str(e)}'}), 500


@transactions_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    """Get a specific transaction"""
    try:
        user_id = int(get_jwt_identity())
        transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        return jsonify({'transaction': transaction.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transactions_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    """Update a transaction"""
    try:
        user_id = int(get_jwt_identity())
        transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'amount' in data:
            transaction.amount = data['amount']
        if 'type' in data:
            transaction.type = data['type']
        if 'category_id' in data:
            transaction.category_id = data['category_id']
        if 'description' in data:
            transaction.description = data['description']
        if 'transaction_date' in data:
            transaction.transaction_date = datetime.fromisoformat(data['transaction_date']).date()
        if 'merchant' in data:
            transaction.merchant = data['merchant']
        if 'payment_method' in data:
            transaction.payment_method = data['payment_method']
        if 'is_recurring' in data:
            transaction.is_recurring = data['is_recurring']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction updated successfully',
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    """Delete a transaction"""
    try:
        user_id = int(get_jwt_identity())
        transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        db.session.delete(transaction)
        db.session.commit()
        
        return jsonify({'message': 'Transaction deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
