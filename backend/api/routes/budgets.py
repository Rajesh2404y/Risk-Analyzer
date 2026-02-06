"""
Budget API Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import db, Budget
from datetime import datetime

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('', methods=['GET'])
@jwt_required()
def get_budgets():
    """Get all budgets for user"""
    try:
        user_id = int(get_jwt_identity())
        budgets = Budget.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'budgets': [b.to_dict() for b in budgets]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@budgets_bp.route('', methods=['POST'])
@jwt_required()
def create_budget():
    """Create a new budget"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validation
        if not data.get('category_id') or not data.get('amount'):
            return jsonify({'error': 'Category and amount are required'}), 400
        
        # Create budget
        budget = Budget(
            user_id=user_id,
            category_id=data['category_id'],
            amount=data['amount'],
            period=data.get('period', 'monthly'),
            start_date=datetime.fromisoformat(data['start_date']).date() if data.get('start_date') else None,
            end_date=datetime.fromisoformat(data['end_date']).date() if data.get('end_date') else None
        )
        
        db.session.add(budget)
        db.session.commit()
        
        return jsonify({
            'message': 'Budget created successfully',
            'budget': budget.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@budgets_bp.route('/<int:budget_id>', methods=['PUT'])
@jwt_required()
def update_budget(budget_id):
    """Update a budget"""
    try:
        user_id = int(get_jwt_identity())
        budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
        
        if not budget:
            return jsonify({'error': 'Budget not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'amount' in data:
            budget.amount = data['amount']
        if 'period' in data:
            budget.period = data['period']
        if 'start_date' in data:
            budget.start_date = datetime.fromisoformat(data['start_date']).date()
        if 'end_date' in data:
            budget.end_date = datetime.fromisoformat(data['end_date']).date()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Budget updated successfully',
            'budget': budget.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@budgets_bp.route('/<int:budget_id>', methods=['DELETE'])
@jwt_required()
def delete_budget(budget_id):
    """Delete a budget"""
    try:
        user_id = int(get_jwt_identity())
        budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
        
        if not budget:
            return jsonify({'error': 'Budget not found'}), 404
        
        db.session.delete(budget)
        db.session.commit()
        
        return jsonify({'message': 'Budget deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
