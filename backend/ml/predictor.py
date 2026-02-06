"""
Expense Prediction Module
Uses time series forecasting to predict future expenses
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import func
from database.models import Transaction, db

class ExpensePredictor:
    def __init__(self):
        """Initialize the predictor"""
        pass
    
    def predict_expenses(self, user_id, months_ahead=3):
        """Predict future expenses using simple moving average and trend analysis"""
        try:
            # Get historical data (last 6 months)
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=180)
            
            # Query daily expenses
            daily_expenses = db.session.query(
                Transaction.transaction_date,
                func.sum(Transaction.amount).label('amount')
            ).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            ).group_by(Transaction.transaction_date).order_by(Transaction.transaction_date).all()
            
            if len(daily_expenses) < 7:
                return self._generate_default_prediction(months_ahead)
            
            # Convert to DataFrame
            df = pd.DataFrame([{
                'date': exp.transaction_date,
                'amount': float(exp.amount)
            } for exp in daily_expenses])
            
            # Resample to weekly for smoother predictions
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            weekly_df = df.resample('W').sum().fillna(0)
            
            # Calculate trend using linear regression
            X = np.arange(len(weekly_df)).reshape(-1, 1)
            y = weekly_df['amount'].values
            
            # Simple linear regression
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X, y)
            
            # Generate future predictions
            future_weeks = months_ahead * 4  # Approximate weeks
            future_X = np.arange(len(weekly_df), len(weekly_df) + future_weeks).reshape(-1, 1)
            predictions = model.predict(future_X)
            
            # Generate dates
            last_date = weekly_df.index[-1]
            future_dates = [last_date + timedelta(weeks=i+1) for i in range(future_weeks)]
            
            # Calculate confidence intervals (simple approach)
            residuals = y - model.predict(X)
            std_error = np.std(residuals)
            
            results = []
            for i, (date, pred) in enumerate(zip(future_dates, predictions)):
                # Ensure non-negative predictions
                pred = max(pred, 0)
                
                results.append({
                    'date': date.date().isoformat(),
                    'predicted_amount': round(float(pred), 2),
                    'confidence_lower': round(float(max(pred - 1.96 * std_error, 0)), 2),
                    'confidence_upper': round(float(pred + 1.96 * std_error), 2),
                    'type': 'weekly'
                })
            
            # Aggregate to monthly
            monthly_results = self._aggregate_to_monthly(results)
            
            return monthly_results
            
        except Exception as e:
            print(f"Error predicting expenses: {e}")
            return self._generate_default_prediction(months_ahead)
    
    def predict_by_category(self, user_id, months_ahead=3):
        """Predict expenses by category"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=180)
            
            # Get category-wise expenses
            category_expenses = db.session.query(
                Transaction.category_id,
                Transaction.transaction_date,
                func.sum(Transaction.amount).label('amount')
            ).filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date,
                Transaction.category_id.isnot(None)
            ).group_by(
                Transaction.category_id,
                Transaction.transaction_date
            ).all()
            
            if not category_expenses:
                return []
            
            # Group by category
            categories = {}
            for exp in category_expenses:
                if exp.category_id not in categories:
                    categories[exp.category_id] = []
                categories[exp.category_id].append({
                    'date': exp.transaction_date,
                    'amount': float(exp.amount)
                })
            
            # Predict for each category
            predictions = []
            for category_id, data in categories.items():
                if len(data) < 5:
                    continue
                
                df = pd.DataFrame(data)
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
                monthly_df = df.resample('ME').sum()
                
                # Simple average for category prediction
                avg_monthly = monthly_df['amount'].mean()
                
                # Generate future months
                last_date = monthly_df.index[-1]
                for i in range(1, months_ahead + 1):
                    future_date = last_date + pd.DateOffset(months=i)
                    predictions.append({
                        'category_id': category_id,
                        'date': future_date.date().isoformat(),
                        'predicted_amount': round(float(avg_monthly), 2)
                    })
            
            return predictions
            
        except Exception as e:
            print(f"Error predicting by category: {e}")
            return []
    
    def _aggregate_to_monthly(self, weekly_results):
        """Aggregate weekly predictions to monthly"""
        try:
            df = pd.DataFrame(weekly_results)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            monthly = df.resample('ME').agg({
                'predicted_amount': 'sum',
                'confidence_lower': 'sum',
                'confidence_upper': 'sum'
            })
            
            return [{
                'date': date.date().isoformat(),
                'predicted_amount': round(row['predicted_amount'], 2),
                'confidence_lower': round(row['confidence_lower'], 2),
                'confidence_upper': round(row['confidence_upper'], 2),
                'type': 'monthly'
            } for date, row in monthly.iterrows()]
        except Exception as e:
            print(f"Error aggregating to monthly: {e}")
            return weekly_results
    
    def _generate_default_prediction(self, months_ahead):
        """Generate default prediction when insufficient data"""
        today = datetime.now().date()
        results = []
        
        for i in range(1, months_ahead + 1):
            future_date = today.replace(day=1) + timedelta(days=32 * i)
            future_date = future_date.replace(day=1)
            
            results.append({
                'date': future_date.isoformat(),
                'predicted_amount': 0,
                'confidence_lower': 0,
                'confidence_upper': 0,
                'type': 'monthly',
                'note': 'insufficient_data'
            })
        
        return results


# Global instance
predictor = ExpensePredictor()
