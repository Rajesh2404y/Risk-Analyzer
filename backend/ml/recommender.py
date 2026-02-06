"""
Recommendation Engine
Generates personalized financial recommendations
"""
from datetime import datetime, timedelta
from sqlalchemy import func
from database.models import Transaction, Budget, Category, db


class RecommendationEngine:
    def __init__(self):
        """Initialize recommendation engine"""
        pass
    
    def generate_recommendations(self, user_id, risk_score_data=None):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Get user financial data
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        # 1. High spending category recommendations
        category_recs = self._analyze_category_spending(user_id, start_date, end_date)
        recommendations.extend(category_recs)
        
        # 2. Budget recommendations
        budget_recs = self._analyze_budget_status(user_id)
        recommendations.extend(budget_recs)
        
        # 3. Savings recommendations
        savings_recs = self._analyze_savings_potential(user_id, start_date, end_date)
        recommendations.extend(savings_recs)
        
        # 4. Risk-based recommendations
        if risk_score_data:
            risk_recs = self._generate_risk_recommendations(risk_score_data)
            recommendations.extend(risk_recs)
        
        # 5. Recurring transaction recommendations
        recurring_recs = self._analyze_recurring_transactions(user_id)
        recommendations.extend(recurring_recs)
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return recommendations[:10]  # Return top 10
    
    def _analyze_category_spending(self, user_id, start_date, end_date):
        """Analyze spending by category"""
        recommendations = []
        
        try:
            # Get category totals
            category_totals = db.session.query(
                Category.name,
                Category.id,
                func.sum(Transaction.amount).label('total')
            ).join(
                Transaction, Transaction.category_id == Category.id
            ).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).group_by(Category.id, Category.name).all()
            
            if not category_totals:
                return recommendations
            
            total_expenses = sum(float(cat.total) for cat in category_totals)
            
            if total_expenses == 0:
                return recommendations
            
            # Find high-spending categories (>30%)
            for cat in category_totals:
                percentage = (float(cat.total) / total_expenses) * 100
                
                if percentage > 30:
                    potential_savings = float(cat.total) * 0.15
                    recommendations.append({
                        'type': 'reduce_spending',
                        'category': cat.name,
                        'title': f'High spending in {cat.name}',
                        'message': f'You\'re spending {percentage:.1f}% of your budget on {cat.name}. Consider reducing by 15%.',
                        'impact': f'Potential savings: ${potential_savings:.2f}/month',
                        'priority': 8 if percentage > 40 else 6,
                        'action': 'reduce'
                    })
        except Exception as e:
            print(f"Error analyzing category spending: {e}")
        
        return recommendations
    
    def _analyze_budget_status(self, user_id):
        """Analyze budget adherence"""
        recommendations = []
        
        try:
            budgets = Budget.query.filter_by(user_id=user_id).all()
            
            for budget in budgets:
                # Get actual spending
                actual = db.session.query(func.sum(Transaction.amount)).filter(
                    Transaction.user_id == user_id,
                    Transaction.category_id == budget.category_id,
                    Transaction.type == 'expense'
                ).scalar() or 0
                
                budget_amount = float(budget.amount)
                actual_amount = float(actual)
                
                # Over budget
                if actual_amount > budget_amount * 1.1:
                    overage = actual_amount - budget_amount
                    percentage = ((actual_amount - budget_amount) / budget_amount) * 100
                    
                    recommendations.append({
                        'type': 'budget_alert',
                        'category': budget.category.name if budget.category else 'Unknown',
                        'title': f'Over budget in {budget.category.name if budget.category else "category"}',
                        'message': f'You\'ve exceeded your budget by ${overage:.2f} ({percentage:.1f}%).',
                        'impact': f'Reduce spending by ${overage:.2f}',
                        'priority': 9,
                        'action': 'alert'
                    })
                
                # Close to budget (90-100%)
                elif actual_amount > budget_amount * 0.9:
                    remaining = budget_amount - actual_amount
                    recommendations.append({
                        'type': 'budget_warning',
                        'category': budget.category.name if budget.category else 'Unknown',
                        'title': f'Approaching budget limit',
                        'message': f'You have ${remaining:.2f} remaining in {budget.category.name if budget.category else "category"}.',
                        'impact': 'Monitor spending carefully',
                        'priority': 5,
                        'action': 'monitor'
                    })
        except Exception as e:
            print(f"Error analyzing budgets: {e}")
        
        return recommendations
    
    def _analyze_savings_potential(self, user_id, start_date, end_date):
        """Analyze savings potential"""
        recommendations = []
        
        try:
            income = db.session.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'income',
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).scalar() or 0
            
            expenses = db.session.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).scalar() or 0
            
            if income > 0:
                savings_rate = ((income - expenses) / income) * 100
                
                if savings_rate < 20:
                    target_savings = income * 0.20
                    current_savings = income - expenses
                    needed = target_savings - current_savings
                    
                    recommendations.append({
                        'type': 'increase_savings',
                        'title': 'Low savings rate',
                        'message': f'Your savings rate is {savings_rate:.1f}%. Aim for at least 20%.',
                        'impact': f'Increase savings by ${needed:.2f}/month',
                        'priority': 7,
                        'action': 'save_more'
                    })
                
                # Negative savings
                if savings_rate < 0:
                    deficit = expenses - income
                    recommendations.append({
                        'type': 'deficit_alert',
                        'title': 'Spending exceeds income',
                        'message': f'You\'re spending ${deficit:.2f} more than you earn.',
                        'impact': 'Critical: Reduce expenses immediately',
                        'priority': 10,
                        'action': 'urgent'
                    })
        except Exception as e:
            print(f"Error analyzing savings: {e}")
        
        return recommendations
    
    def _generate_risk_recommendations(self, risk_data):
        """Generate recommendations based on risk score"""
        recommendations = []
        
        risk_level = risk_data.get('risk_level', 'medium')
        factors = risk_data.get('factors', {})
        
        if risk_level == 'high':
            recommendations.append({
                'type': 'risk_alert',
                'title': 'High financial risk detected',
                'message': 'Your financial health needs immediate attention.',
                'impact': 'Review and act on key risk factors',
                'priority': 9,
                'action': 'review_finances'
            })
        
        # Spending velocity recommendations
        velocity = factors.get('spending_velocity', {})
        if velocity.get('trend', 0) > 15:
            recommendations.append({
                'type': 'spending_trend',
                'title': 'Rapidly increasing spending',
                'message': f'Your spending is trending up by {velocity.get("trend", 0):.1f}%.',
                'impact': 'Review recent purchases',
                'priority': 7,
                'action': 'reduce_trend'
            })
        
        return recommendations
    
    def _analyze_recurring_transactions(self, user_id):
        """Analyze recurring transactions for optimization"""
        recommendations = []
        
        try:
            # Get recurring transactions
            recurring = Transaction.query.filter_by(
                user_id=user_id,
                is_recurring=True,
                type='expense'
            ).all()
            
            total_recurring = sum(float(t.amount) for t in recurring)
            
            if total_recurring > 0 and len(recurring) > 3:
                recommendations.append({
                    'type': 'recurring_review',
                    'title': 'Review recurring expenses',
                    'message': f'You have {len(recurring)} recurring expenses totaling ${total_recurring:.2f}/month.',
                    'impact': 'Potential to reduce or cancel subscriptions',
                    'priority': 6,
                    'action': 'review_subscriptions'
                })
        except Exception as e:
            print(f"Error analyzing recurring transactions: {e}")
        
        return recommendations


# Global instance
recommender = RecommendationEngine()
