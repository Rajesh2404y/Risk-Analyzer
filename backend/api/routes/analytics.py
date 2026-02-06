"""
Analytics API Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import Transaction, Category, db
from sqlalchemy import func
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """Get financial summary"""
    try:
        user_id = int(get_jwt_identity())
        
        # Get date range (default: current month)
        end_date = datetime.now().date()
        start_date = request.args.get('start_date')
        if start_date:
            start_date = datetime.fromisoformat(start_date).date()
        else:
            start_date = end_date.replace(day=1)
        
        # Total income
        total_income = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'income',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).scalar() or 0
        
        # Total expenses
        total_expenses = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).scalar() or 0
        
        # Net savings
        net_savings = total_income - total_expenses
        
        # Transaction count
        transaction_count = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).count()
        
        return jsonify({
            'summary': {
                'total_income': float(total_income),
                'total_expenses': float(total_expenses),
                'net_savings': float(net_savings),
                'transaction_count': transaction_count,
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_trends():
    """Get spending trends over time"""
    try:
        user_id = int(get_jwt_identity())
        
        # Get parameters
        period = request.args.get('period', 'monthly')  # daily, weekly, monthly
        months = request.args.get('months', 6, type=int)
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30 * months)
        
        # Query transactions
        if period == 'daily':
            group_by = func.date(Transaction.transaction_date)
        elif period == 'weekly':
            group_by = func.yearweek(Transaction.transaction_date)
        else:  # monthly
            group_by = func.date_format(Transaction.transaction_date, '%Y-%m')
        
        # Income trend
        income_trend = db.session.query(
            group_by.label('period'),
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'income',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by('period').order_by('period').all()
        
        # Expense trend
        expense_trend = db.session.query(
            group_by.label('period'),
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by('period').order_by('period').all()
        
        return jsonify({
            'trends': {
                'income': [{
                    'period': str(item.period) if item.period else None,
                    'amount': float(item.total)
                } for item in income_trend],
                'expenses': [{
                    'period': str(item.period) if item.period else None,
                    'amount': float(item.total)
                } for item in expense_trend]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/category-breakdown', methods=['GET'])
@jwt_required()
def get_category_breakdown():
    """Get expense breakdown by category"""
    try:
        user_id = int(get_jwt_identity())
        
        # Get date range
        end_date = datetime.now().date()
        start_date = request.args.get('start_date')
        if start_date:
            start_date = datetime.fromisoformat(start_date).date()
        else:
            start_date = end_date - timedelta(days=30)
        
        # Query category breakdown
        breakdown = db.session.query(
            Category.id,
            Category.name,
            Category.color,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count')
        ).join(
            Transaction, Transaction.category_id == Category.id
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by(Category.id, Category.name, Category.color).all()
        
        total = sum(float(item.total) for item in breakdown)
        
        categories = [{
            'category_id': item.id,
            'category_name': item.name,
            'color': item.color,
            'amount': float(item.total),
            'percentage': (float(item.total) / total * 100) if total > 0 else 0,
            'transaction_count': item.count
        } for item in breakdown]
        
        return jsonify({
            'breakdown': categories,
            'total': total
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/comparison', methods=['GET'])
@jwt_required()
def get_comparison():
    """Compare spending between periods"""
    try:
        user_id = int(get_jwt_identity())
        
        # Current month
        current_end = datetime.now().date()
        current_start = current_end.replace(day=1)
        
        # Previous month
        previous_end = (current_start - timedelta(days=1))
        previous_start = previous_end.replace(day=1)
        
        # Current month expenses
        current_expenses = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.transaction_date >= current_start,
            Transaction.transaction_date <= current_end
        ).scalar() or 0
        
        # Previous month expenses
        previous_expenses = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.transaction_date >= previous_start,
            Transaction.transaction_date <= previous_end
        ).scalar() or 0
        
        # Calculate change
        change = current_expenses - previous_expenses
        change_percentage = (change / previous_expenses * 100) if previous_expenses > 0 else 0
        
        return jsonify({
            'comparison': {
                'current_period': {
                    'start': current_start.isoformat(),
                    'end': current_end.isoformat(),
                    'total': float(current_expenses)
                },
                'previous_period': {
                    'start': previous_start.isoformat(),
                    'end': previous_end.isoformat(),
                    'total': float(previous_expenses)
                },
                'change': float(change),
                'change_percentage': round(change_percentage, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
