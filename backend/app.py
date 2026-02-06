"""
Main Flask Application Entry Point
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    JWTManager(app)
    
    # Initialize database
    from database.models import db
    db.init_app(app)
    
    # Register blueprints
    from api.routes.auth import auth_bp
    from api.routes.transactions import transactions_bp
    from api.routes.analytics import analytics_bp
    from api.routes.predictions import predictions_bp
    from api.routes.recommendations import recommendations_bp
    from api.routes.budgets import budgets_bp
    from api.routes.categories import categories_bp, risk_bp
    from api.routes.ai_insights import ai_insights_bp
    from api.routes.upload import upload_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
    app.register_blueprint(budgets_bp, url_prefix='/api/budgets')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(risk_bp, url_prefix='/api/risk')
    app.register_blueprint(ai_insights_bp, url_prefix='/api/ai-insights')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    
    # Create tables
    with app.app_context():
        db.create_all()
        # Initialize default categories
        from database.models import initialize_default_categories
        initialize_default_categories()
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Expense Analyzer API is running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
