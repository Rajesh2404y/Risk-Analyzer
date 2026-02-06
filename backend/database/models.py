"""
SQLAlchemy Database Models
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import JSON
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
    budgets = db.relationship('Budget', backref='user', lazy=True, cascade='all, delete-orphan')
    risk_scores = db.relationship('RiskScore', backref='user', lazy=True, cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', backref='user', uselist=False, cascade='all, delete-orphan')
    categories = db.relationship('Category', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Category(db.Model):
    """Category model for transactions"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    icon = db.Column(db.String(50))
    color = db.Column(db.String(20))
    is_system = db.Column(db.Boolean, default=False)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='category', lazy=True)
    budgets = db.relationship('Budget', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'icon': self.icon,
            'color': self.color,
            'is_system': self.is_system
        }


class Transaction(db.Model):
    """Transaction model for income and expenses"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    description = db.Column(db.Text)
    transaction_date = db.Column(db.Date, nullable=False)
    merchant = db.Column(db.String(255))
    payment_method = db.Column(db.String(50))
    is_recurring = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'amount': float(self.amount),
            'category': self.category.to_dict() if self.category else None,
            'description': self.description,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'merchant': self.merchant,
            'payment_method': self.payment_method,
            'is_recurring': self.is_recurring,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Budget(db.Model):
    """Budget model"""
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    period = db.Column(db.String(20), default='monthly')  # 'weekly', 'monthly', 'yearly'
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category.to_dict() if self.category else None,
            'amount': float(self.amount),
            'period': self.period,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None
        }


class RiskScore(db.Model):
    """Risk score model"""
    __tablename__ = 'risk_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 0-100
    risk_level = db.Column(db.String(20))  # 'low', 'medium', 'high'
    factors = db.Column(JSON)  # Detailed breakdown
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'score': self.score,
            'risk_level': self.risk_level,
            'factors': self.factors,
            'calculated_at': self.calculated_at.isoformat() if self.calculated_at else None
        }


class Prediction(db.Model):
    """Prediction model for future expenses"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prediction_date = db.Column(db.Date, nullable=False)
    predicted_amount = db.Column(db.Numeric(10, 2))
    confidence_lower = db.Column(db.Numeric(10, 2))
    confidence_upper = db.Column(db.Numeric(10, 2))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'prediction_date': self.prediction_date.isoformat() if self.prediction_date else None,
            'predicted_amount': float(self.predicted_amount) if self.predicted_amount else None,
            'confidence_lower': float(self.confidence_lower) if self.confidence_lower else None,
            'confidence_upper': float(self.confidence_upper) if self.confidence_upper else None,
            'category': self.category.to_dict() if self.category else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserPreference(db.Model):
    """User preferences model"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    currency = db.Column(db.String(10), default='USD')
    notification_enabled = db.Column(db.Boolean, default=True)
    risk_alert_threshold = db.Column(db.Integer, default=60)
    theme = db.Column(db.String(20), default='light')
    phone_number = db.Column(db.String(20))  # For SMS alerts
    sms_alerts_enabled = db.Column(db.Boolean, default=False)
    preferences = db.Column(JSON)  # Additional settings
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'currency': self.currency,
            'notification_enabled': self.notification_enabled,
            'risk_alert_threshold': self.risk_alert_threshold,
            'theme': self.theme,
            'phone_number': self.phone_number,
            'sms_alerts_enabled': self.sms_alerts_enabled,
            'preferences': self.preferences
        }


class FileUpload(db.Model):
    """File upload model for tracking uploaded statements"""
    __tablename__ = 'file_uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)  # 'csv', 'excel', 'pdf'
    file_size = db.Column(db.Integer)  # Size in bytes
    status = db.Column(db.String(20), default='pending')  # 'pending', 'processing', 'completed', 'failed'
    transactions_count = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
    processing_details = db.Column(JSON)  # Detailed processing info
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('file_uploads', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'status': self.status,
            'transactions_count': self.transactions_count,
            'error_message': self.error_message,
            'processing_details': self.processing_details,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }


def initialize_default_categories():
    """Initialize default system categories"""
    default_categories = [
        # Expense categories
        {'name': 'Food & Dining', 'type': 'expense', 'icon': 'restaurant', 'color': '#FF6384', 'is_system': True},
        {'name': 'Transportation', 'type': 'expense', 'icon': 'directions_car', 'color': '#36A2EB', 'is_system': True},
        {'name': 'Shopping', 'type': 'expense', 'icon': 'shopping_cart', 'color': '#FFCE56', 'is_system': True},
        {'name': 'Bills & Utilities', 'type': 'expense', 'icon': 'receipt', 'color': '#4BC0C0', 'is_system': True},
        {'name': 'Healthcare', 'type': 'expense', 'icon': 'local_hospital', 'color': '#9966FF', 'is_system': True},
        {'name': 'Entertainment', 'type': 'expense', 'icon': 'movie', 'color': '#FF9F40', 'is_system': True},
        {'name': 'Education', 'type': 'expense', 'icon': 'school', 'color': '#FF6384', 'is_system': True},
        {'name': 'Others', 'type': 'expense', 'icon': 'category', 'color': '#C9CBCF', 'is_system': True},
        
        # Income categories
        {'name': 'Salary', 'type': 'income', 'icon': 'payments', 'color': '#4CAF50', 'is_system': True},
        {'name': 'Business', 'type': 'income', 'icon': 'business', 'color': '#2196F3', 'is_system': True},
        {'name': 'Investments', 'type': 'income', 'icon': 'trending_up', 'color': '#FFC107', 'is_system': True},
        {'name': 'Other Income', 'type': 'income', 'icon': 'attach_money', 'color': '#9C27B0', 'is_system': True},
    ]
    
    for cat_data in default_categories:
        existing = Category.query.filter_by(name=cat_data['name'], is_system=True, user_id=None).first()
        if not existing:
            category = Category(**cat_data, user_id=None)
            db.session.add(category)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing categories: {e}")
