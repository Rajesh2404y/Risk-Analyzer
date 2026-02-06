"""
Add Sample Transactions for Testing
This will populate your account with realistic transaction data
"""
import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from database.models import db, Transaction, Category, User

def add_sample_data(user_email):
    """Add sample transactions for a user"""
    
    app = create_app()
    
    with app.app_context():
        # Get user
        user = User.query.filter_by(email=user_email).first()
        if not user:
            print(f"❌ User not found: {user_email}")
            print("Please register first at http://localhost:5173/register")
            return False
        
        print(f"✅ Found user: {user.email}")
        
        # Get categories
        food_cat = Category.query.filter_by(name='Food & Dining', is_system=True).first()
        transport_cat = Category.query.filter_by(name='Transportation', is_system=True).first()
        shopping_cat = Category.query.filter_by(name='Shopping', is_system=True).first()
        bills_cat = Category.query.filter_by(name='Bills & Utilities', is_system=True).first()
        salary_cat = Category.query.filter_by(name='Salary', is_system=True).first()
        
        # Sample transactions for last 3 months
        today = datetime.now().date()
        transactions = []
        
        # Month 1 (3 months ago)
        month1_start = today - timedelta(days=90)
        transactions.extend([
            # Income
            Transaction(user_id=user.id, type='income', amount=Decimal('5000.00'), 
                       category_id=salary_cat.id, description='Monthly Salary',
                       transaction_date=month1_start, merchant='Company Inc'),
            # Expenses
            Transaction(user_id=user.id, type='expense', amount=Decimal('1200.00'),
                       category_id=bills_cat.id, description='Rent',
                       transaction_date=month1_start + timedelta(days=1), merchant='Landlord'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('150.00'),
                       category_id=bills_cat.id, description='Electricity Bill',
                       transaction_date=month1_start + timedelta(days=5), merchant='Power Company'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('80.00'),
                       category_id=transport_cat.id, description='Gas',
                       transaction_date=month1_start + timedelta(days=7), merchant='Gas Station'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('250.00'),
                       category_id=food_cat.id, description='Groceries',
                       transaction_date=month1_start + timedelta(days=10), merchant='Supermarket'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('120.00'),
                       category_id=shopping_cat.id, description='Clothes',
                       transaction_date=month1_start + timedelta(days=15), merchant='Fashion Store'),
        ])
        
        # Month 2 (2 months ago)
        month2_start = today - timedelta(days=60)
        transactions.extend([
            # Income
            Transaction(user_id=user.id, type='income', amount=Decimal('5000.00'),
                       category_id=salary_cat.id, description='Monthly Salary',
                       transaction_date=month2_start, merchant='Company Inc'),
            # Expenses
            Transaction(user_id=user.id, type='expense', amount=Decimal('1200.00'),
                       category_id=bills_cat.id, description='Rent',
                       transaction_date=month2_start + timedelta(days=1), merchant='Landlord'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('160.00'),
                       category_id=bills_cat.id, description='Electricity Bill',
                       transaction_date=month2_start + timedelta(days=5), merchant='Power Company'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('90.00'),
                       category_id=transport_cat.id, description='Gas',
                       transaction_date=month2_start + timedelta(days=7), merchant='Gas Station'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('280.00'),
                       category_id=food_cat.id, description='Groceries',
                       transaction_date=month2_start + timedelta(days=10), merchant='Supermarket'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('200.00'),
                       category_id=shopping_cat.id, description='Electronics',
                       transaction_date=month2_start + timedelta(days=15), merchant='Tech Store'),
        ])
        
        # Month 3 (1 month ago)
        month3_start = today - timedelta(days=30)
        transactions.extend([
            # Income
            Transaction(user_id=user.id, type='income', amount=Decimal('5000.00'),
                       category_id=salary_cat.id, description='Monthly Salary',
                       transaction_date=month3_start, merchant='Company Inc'),
            # Expenses
            Transaction(user_id=user.id, type='expense', amount=Decimal('1200.00'),
                       category_id=bills_cat.id, description='Rent',
                       transaction_date=month3_start + timedelta(days=1), merchant='Landlord'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('170.00'),
                       category_id=bills_cat.id, description='Electricity Bill',
                       transaction_date=month3_start + timedelta(days=5), merchant='Power Company'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('100.00'),
                       category_id=transport_cat.id, description='Gas',
                       transaction_date=month3_start + timedelta(days=7), merchant='Gas Station'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('300.00'),
                       category_id=food_cat.id, description='Groceries',
                       transaction_date=month3_start + timedelta(days=10), merchant='Supermarket'),
            Transaction(user_id=user.id, type='expense', amount=Decimal('150.00'),
                       category_id=shopping_cat.id, description='Books',
                       transaction_date=month3_start + timedelta(days=15), merchant='Bookstore'),
        ])
        
        # Add all transactions
        for transaction in transactions:
            db.session.add(transaction)
        
        try:
            db.session.commit()
            print(f"\n✅ SUCCESS! Added {len(transactions)} sample transactions")
            print("\nSummary:")
            print(f"  • Income: $15,000 (3 months)")
            print(f"  • Expenses: ~$5,500 (3 months)")
            print(f"  • Savings Rate: ~63%")
            print("\nNow you can:")
            print("  1. View Dashboard - See real financial data")
            print("  2. Check Analytics - View spending trends")
            print("  3. Risk Score - Get actual risk assessment")
            print("  4. Predictions - See expense forecasts")
            print("\nGo to: http://localhost:5173/dashboard")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_sample_data.py YOUR_EMAIL")
        print("Example: python add_sample_data.py user@example.com")
    else:
        email = sys.argv[1]
        add_sample_data(email)
