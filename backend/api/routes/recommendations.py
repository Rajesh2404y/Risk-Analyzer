"""
Recommendations API Routes
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ml.risk_calculator import risk_calculator
from database.models import User, UserPreference, Transaction, db
from services.email_service import email_service
from sqlalchemy import func
from datetime import datetime, timedelta

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get personalized recommendations"""
    try:
        user_id = int(get_jwt_identity())
        
        # Check if user has any transactions
        transaction_count = db.session.query(func.count(Transaction.id)).filter(
            Transaction.user_id == user_id
        ).scalar() or 0
        
        if transaction_count == 0:
            return jsonify({
                'recommendations': [],
                'risk_context': {'score': 0, 'level': 'unknown'},
                'message': 'Add transactions to get personalized recommendations'
            }), 200
        
        # Calculate current risk score
        try:
            risk_score = risk_calculator.calculate_risk_score(user_id)
        except Exception as risk_error:
            print(f"Risk calculation error: {risk_error}")
            risk_score = {'score': 50, 'risk_level': 'medium', 'factors': {}}
        
        # Generate recommendations based on actual risk
        recommendations = []
        
        if risk_score['score'] >= 60:
            recommendations.append({
                'type': 'high_risk',
                'title': 'High Financial Risk Detected',
                'description': 'Your spending patterns indicate high financial risk',
                'priority': 'high',
                'action': 'Review your expenses and create a budget'
            })
        elif risk_score['score'] >= 40:
            recommendations.append({
                'type': 'medium_risk',
                'title': 'Moderate Financial Risk',
                'description': 'Some areas need attention',
                'priority': 'medium',
                'action': 'Monitor your spending closely'
            })
        
        return jsonify({
            'recommendations': recommendations,
            'risk_context': {
                'score': risk_score['score'],
                'level': risk_score['risk_level']
            }
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Recommendations error: {traceback.format_exc()}")
        return jsonify({
            'recommendations': [],
            'risk_context': {'score': 0, 'level': 'unknown'},
            'error': str(e)
        }), 200


@recommendations_bp.route('/test-email', methods=['POST'])
@jwt_required()
def test_email():
    """Test email configuration"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check email config
        if not email_service.is_configured():
            return jsonify({'error': 'Email not configured'}), 503
        
        # Send simple test email
        test_recs = [{
            'type': 'test',
            'title': 'Test Alert',
            'message': 'This is a test email from AI Expense Risk Analyzer',
            'impact': 'Testing email functionality',
            'priority': 8
        }]
        
        success = email_service.send_recommendation_alert(
            user_email=user.email,
            user_name=user.full_name or 'User',
            recommendations=test_recs
        )
        
        if success:
            return jsonify({'message': f'Test email sent to {user.email}', 'sent': True}), 200
        else:
            return jsonify({'error': 'Email send failed', 'sent': False}), 500
            
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/send-alerts', methods=['POST'])
@jwt_required()
def send_recommendation_alerts():
    """Send recommendation alerts via email based on AI risk analysis"""
    try:
        user_id = int(get_jwt_identity())
        
        # Get user details
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if email service is configured
        from services.email_service import email_service
        
        if not email_service.is_configured():
            return jsonify({
                'error': 'Email service not configured. Set SMTP settings in .env file.',
                'sent': False
            }), 503
        
        # Calculate financial metrics
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        total_income = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'income',
            Transaction.transaction_date >= start_date
        ).scalar() or 0
        
        total_expenses = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.transaction_date >= start_date
        ).scalar() or 0
        
        savings_rate = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
        
        # Calculate risk score
        risk_score = 0
        if savings_rate < 10:
            risk_score = 80
        elif savings_rate < 20:
            risk_score = 60
        elif savings_rate < 30:
            risk_score = 40
        else:
            risk_score = 20
        
        # Generate recommendations
        recommendations = []
        
        if risk_score >= 60:
            recommendations.append({
                'type': 'critical_alert',
                'title': '🚨 Critical: Low Savings Rate',
                'message': f'Savings rate: {savings_rate:.1f}%. Spending ${total_expenses:.2f} vs income ${total_income:.2f}',
                'impact': 'Risk of financial instability',
                'priority': 9
            })
            recommendations.append({
                'type': 'expense_reduction',
                'title': '💰 Reduce Expenses',
                'message': 'Cut non-essential spending by 15-20%',
                'impact': f'Save ${total_expenses * 0.15:.2f}/month',
                'priority': 8
            })
        elif risk_score >= 40:
            recommendations.append({
                'type': 'warning',
                'title': '⚠️ Moderate Risk',
                'message': f'Savings rate {savings_rate:.1f}% needs improvement',
                'impact': 'Optimize spending patterns',
                'priority': 7
            })
        
        recommendations.append({
            'type': 'emergency_fund',
            'title': '🏦 Build Emergency Fund',
            'message': 'Maintain 6 months expenses as savings',
            'impact': f'Target: ${total_expenses * 6:.2f}',
            'priority': 7
        })
        
        high_priority = [r for r in recommendations if r.get('priority', 0) >= 7]
        
        if not high_priority:
            return jsonify({
                'message': 'No high-priority alerts. Finances are healthy!',
                'sent': False,
                'risk_score': risk_score
            }), 200
        
        # Send email
        email_sent = email_service.send_recommendation_alert(
            user_email=user.email,
            user_name=user.full_name or user.email.split('@')[0],
            recommendations=recommendations
        )
        
        if email_sent:
            return jsonify({
                'message': f'Alert sent to {user.email}',
                'sent': True,
                'risk_score': risk_score,
                'risk_level': 'High' if risk_score >= 60 else 'Medium' if risk_score >= 40 else 'Low',
                'recommendations_count': len(high_priority),
                'analysis': {
                    'income': float(total_income),
                    'expenses': float(total_expenses),
                    'savings_rate': round(savings_rate, 2)
                }
            }), 200
        else:
            return jsonify({
                'error': 'Failed to send email. Check SMTP configuration.',
                'sent': False
            }), 500
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': f'Server error: {str(e)}'}), 500
