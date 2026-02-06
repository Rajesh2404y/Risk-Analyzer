"""
Predictions API Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from dateutil.relativedelta import relativedelta
from database.models import Transaction, db
from sqlalchemy import func

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/expenses', methods=['GET'])
@jwt_required()
def predict_expenses():
    """Predict future expenses"""
    try:
        user_id = int(get_jwt_identity())
        months_ahead = request.args.get('months', 6, type=int)
        
        # Check if user has transactions
        transaction_count = db.session.query(func.count(Transaction.id)).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense'
        ).scalar() or 0
        
        if transaction_count < 3:
            # Not enough data for predictions
            return jsonify({
                'predictions': [],
                'months_ahead': months_ahead,
                'message': 'Add more transactions to enable predictions'
            }), 200
        
        # Calculate average monthly expenses from last 3 months
        three_months_ago = datetime.now().date() - relativedelta(months=3)
        avg_expense = db.session.query(func.avg(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.transaction_date >= three_months_ago
        ).scalar() or 0
        
        # Generate predictions
        predictions = []
        current_date = datetime.now()
        
        for i in range(1, months_ahead + 1):
            future_date = current_date + relativedelta(months=i)
            # Simple prediction: use average with slight variation
            predicted = float(avg_expense) * (1 + (i * 0.02))  # 2% increase per month
            
            predictions.append({
                'date': future_date.strftime('%Y-%m-%d'),
                'predicted_amount': round(predicted, 2)
            })
        
        return jsonify({
            'predictions': predictions,
            'months_ahead': months_ahead
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Predictions error: {traceback.format_exc()}")
        return jsonify({'error': str(e), 'predictions': []}), 200


@predictions_bp.route('/by-category', methods=['GET'])
@jwt_required()
def predict_by_category():
    """Predict expenses by category"""
    try:
        user_id = int(get_jwt_identity())
        
        return jsonify({
            'predictions': [],
            'message': 'Category predictions not yet implemented'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
