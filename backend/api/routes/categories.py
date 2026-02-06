"""
Category API Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import db, Category, Transaction
from ml.risk_calculator import risk_calculator

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories (system + user custom)"""
    try:
        user_id = int(get_jwt_identity())
        
        # Get system categories
        system_categories = Category.query.filter_by(is_system=True, user_id=None).all()
        
        # Get user custom categories
        user_categories = Category.query.filter_by(user_id=user_id, is_system=False).all()
        
        all_categories = system_categories + user_categories
        
        return jsonify({
            'categories': [c.to_dict() for c in all_categories]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@categories_bp.route('', methods=['POST'])
@jwt_required()
def create_category():
    """Create a custom category"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validation
        if not data.get('name') or not data.get('type'):
            return jsonify({'error': 'Name and type are required'}), 400
        
        # Create category
        category = Category(
            user_id=user_id,
            name=data['name'],
            type=data['type'],
            icon=data.get('icon', 'category'),
            color=data.get('color', '#9E9E9E'),
            is_system=False
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@categories_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """Update a custom category"""
    try:
        user_id = int(get_jwt_identity())
        category = Category.query.filter_by(id=category_id, user_id=user_id, is_system=False).first()
        
        if not category:
            return jsonify({'error': 'Category not found or is a system category'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            category.name = data['name']
        if 'icon' in data:
            category.icon = data['icon']
        if 'color' in data:
            category.color = data['color']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Category updated successfully',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """Delete a custom category"""
    try:
        user_id = int(get_jwt_identity())
        category = Category.query.filter_by(id=category_id, user_id=user_id, is_system=False).first()
        
        if not category:
            return jsonify({'error': 'Category not found or is a system category'}), 404
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({'message': 'Category deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Risk score endpoint
from flask import Blueprint as BP
risk_bp = BP('risk', __name__)

@risk_bp.route('/score', methods=['GET'])
@jwt_required()
def get_risk_score():
    """Get current risk score"""
    try:
        user_id = int(get_jwt_identity())
        
        # Check if user has transactions
        from sqlalchemy import func
        transaction_count = db.session.query(func.count(Transaction.id)).filter(
            Transaction.user_id == user_id
        ).scalar() or 0
        
        if transaction_count == 0:
            # No transactions, return default
            return jsonify({
                'score': 0,
                'risk_level': 'unknown',
                'factors': {},
                'message': 'Add transactions to calculate risk score'
            }), 200
        
        try:
            risk_data = risk_calculator.calculate_risk_score(user_id)
        except Exception as calc_error:
            print(f"Risk calculation error: {calc_error}")
            import traceback
            print(traceback.format_exc())
            risk_data = {
                'score': 50,
                'risk_level': 'medium',
                'factors': {},
                'message': 'Unable to calculate detailed risk score'
            }
        
        # Convert any Decimal values to float in factors
        from decimal import Decimal
        
        def convert_decimals(obj):
            if isinstance(obj, dict):
                return {k: convert_decimals(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_decimals(item) for item in obj]
            elif isinstance(obj, Decimal):
                return float(obj)
            return obj
        
        factors = convert_decimals(risk_data.get('factors', {}))
        
        # Save to database
        from database.models import RiskScore
        try:
            risk_score = RiskScore(
                user_id=user_id,
                score=risk_data['score'],
                risk_level=risk_data['risk_level'],
                factors=factors
            )
            db.session.add(risk_score)
            db.session.commit()
        except Exception as db_error:
            print(f"Database save error: {db_error}")
            db.session.rollback()
        
        return jsonify({
            'score': risk_data['score'],
            'risk_level': risk_data['risk_level'],
            'factors': factors
        }), 200
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Risk score error: {traceback.format_exc()}")
        return jsonify({
            'score': 0,
            'risk_level': 'unknown',
            'factors': {},
            'message': 'Error calculating risk score'
        }), 200


# Register risk blueprint in app.py
