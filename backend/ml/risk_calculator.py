"""
Risk Score Calculator
Calculates financial risk score based on multiple factors
"""
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import func
from database.models import Transaction, Budget, db


class RiskCalculator:
    def __init__(self):
        """Initialize risk calculator with weights"""
        self.weights = {
            'spending_velocity': 0.25,
            'debt_to_income': 0.20,
            'savings_rate': 0.20,
            'emergency_fund': 0.15,
            'budget_adherence': 0.10,
            'category_concentration': 0.10
        }
    
    def calculate_risk_score(self, user_id):
        """Calculate comprehensive risk score for a user"""
        factors = {}
        score = 0
        
        # Get user data
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=90)  # Last 3 months
        
        # 1. Spending Velocity (0-25 points)
        velocity_score, velocity_data = self._calculate_spending_velocity(user_id, start_date, end_date)
        score += velocity_score
        factors['spending_velocity'] = velocity_data
        
        # 2. Savings Rate (0-20 points, inverse)
        savings_score, savings_data = self._calculate_savings_rate(user_id, start_date, end_date)
        score += savings_score
        factors['savings_rate'] = savings_data
        
        # 3. Budget Adherence (0-10 points)
        budget_score, budget_data = self._calculate_budget_adherence(user_id)
        score += budget_score
        factors['budget_adherence'] = budget_data
        
        # 4. Category Concentration (0-10 points)
        concentration_score, concentration_data = self._calculate_category_concentration(user_id, start_date, end_date)
        score += concentration_score
        factors['category_concentration'] = concentration_data
        
        # 5. Emergency Fund (0-15 points, inverse) - Placeholder
        emergency_score = 10  # Default medium score
        factors['emergency_fund'] = {
            'score': emergency_score,
            'months_covered': 0,
            'note': 'Emergency fund tracking not implemented'
        }
        score += emergency_score
        
        # 6. Debt to Income (0-20 points) - Placeholder
        debt_score = 5  # Default low score
        factors['debt_to_income'] = {
            'score': debt_score,
            'ratio': 0,
            'note': 'Debt tracking not implemented'
        }
        score += debt_score
        
        # Determine risk level
        risk_level = self._get_risk_level(score)
        
        return {
            'score': min(int(score), 100),
            'risk_level': risk_level,
            'factors': factors
        }
    
    def _calculate_spending_velocity(self, user_id, start_date, end_date):
        """Calculate spending velocity (rate of increase)"""
        try:
            # Get monthly expenses - MySQL compatible
            expenses = db.session.query(
                func.date_format(Transaction.transaction_date, '%Y-%m').label('month'),
                func.sum(Transaction.amount).label('total')
            ).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).group_by('month').order_by('month').all()
            
            if len(expenses) < 2:
                return 5, {'score': 5, 'trend': 'insufficient_data'}
            
            amounts = [float(exp.total) for exp in expenses]
            avg = np.mean(amounts)
            
            if avg == 0:
                return 0, {'score': 0, 'trend': 'no_expenses'}
            
            # Calculate trend (positive = increasing spending)
            trend = (amounts[-1] - amounts[0]) / avg * 100
            
            # Score: higher trend = higher risk
            if trend > 20:
                score = 25
            elif trend > 10:
                score = 20
            elif trend > 0:
                score = 15
            elif trend > -10:
                score = 10
            else:
                score = 5
            
            return score, {
                'score': score,
                'trend': round(trend, 2),
                'average_monthly': round(avg, 2),
                'last_month': round(amounts[-1], 2)
            }
        except Exception as e:
            print(f"Error calculating spending velocity: {e}")
            return 10, {'score': 10, 'error': str(e)}
    
    def _calculate_savings_rate(self, user_id, start_date, end_date):
        """Calculate savings rate (income - expenses) / income"""
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
            
            if income == 0:
                return 15, {'score': 15, 'rate': 0, 'note': 'no_income'}
            
            savings = income - expenses
            rate = (savings / income) * 100
            
            # Score: lower savings = higher risk (inverse)
            if rate < 0:
                score = 20  # Spending more than income!
            elif rate < 10:
                score = 18
            elif rate < 20:
                score = 15
            elif rate < 30:
                score = 10
            else:
                score = 5
            
            return score, {
                'score': score,
                'rate': round(rate, 2),
                'income': float(income),
                'expenses': float(expenses),
                'savings': float(savings)
            }
        except Exception as e:
            print(f"Error calculating savings rate: {e}")
            return 10, {'score': 10, 'error': str(e)}
    
    def _calculate_budget_adherence(self, user_id):
        """Calculate how well user adheres to budgets"""
        try:
            budgets = Budget.query.filter_by(user_id=user_id).all()
            
            if not budgets:
                return 5, {'score': 5, 'note': 'no_budgets_set'}
            
            variances = []
            for budget in budgets:
                # Get actual spending for category
                actual = db.session.query(func.sum(Transaction.amount)).filter(
                    Transaction.user_id == user_id,
                    Transaction.category_id == budget.category_id,
                    Transaction.type == 'expense'
                ).scalar() or 0
                
                budget_amount = float(budget.amount)
                if budget_amount > 0:
                    variance = ((actual - budget_amount) / budget_amount) * 100
                    variances.append(variance)
            
            if not variances:
                return 5, {'score': 5, 'note': 'no_variance_data'}
            
            avg_variance = np.mean(variances)
            
            # Score: higher variance = higher risk
            if avg_variance > 50:
                score = 10
            elif avg_variance > 25:
                score = 8
            elif avg_variance > 10:
                score = 5
            elif avg_variance > -10:
                score = 3
            else:
                score = 0
            
            return score, {
                'score': score,
                'average_variance': round(avg_variance, 2),
                'budgets_count': len(budgets)
            }
        except Exception as e:
            print(f"Error calculating budget adherence: {e}")
            return 5, {'score': 5, 'error': str(e)}
    
    def _calculate_category_concentration(self, user_id, start_date, end_date):
        """Calculate if spending is concentrated in one category"""
        try:
            category_totals = db.session.query(
                Transaction.category_id,
                func.sum(Transaction.amount).label('total')
            ).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).group_by(Transaction.category_id).all()
            
            if not category_totals:
                return 0, {'score': 0, 'note': 'no_expenses'}
            
            amounts = [float(cat.total) for cat in category_totals]
            total = sum(amounts)
            
            if total == 0:
                return 0, {'score': 0, 'note': 'no_expenses'}
            
            # Calculate max percentage
            max_percentage = (max(amounts) / total) * 100
            
            # Score: higher concentration = higher risk
            if max_percentage > 60:
                score = 10
            elif max_percentage > 50:
                score = 8
            elif max_percentage > 40:
                score = 5
            else:
                score = 2
            
            return score, {
                'score': score,
                'max_percentage': round(max_percentage, 2),
                'categories_count': len(category_totals)
            }
        except Exception as e:
            print(f"Error calculating category concentration: {e}")
            return 5, {'score': 5, 'error': str(e)}
    
    def _get_risk_level(self, score):
        """Determine risk level based on score"""
        if score <= 30:
            return 'low'
        elif score <= 60:
            return 'medium'
        else:
            return 'high'


# Global instance
risk_calculator = RiskCalculator()
