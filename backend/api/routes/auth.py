"""
Authentication API Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database.models import db, User, UserPreference

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Check if user exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        
        # Create user
        user = User(
            email=data['email'],
            full_name=data.get('full_name', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create default preferences
        preferences = UserPreference(user_id=user.id)
        db.session.add(preferences)
        db.session.commit()
        
        # Generate token (identity must be string for Flask-JWT-Extended)
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token (identity must be string for Flask-JWT-Extended)
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validation
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        # Find user
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Set new password
        user.set_password(data['new_password'])
        
        # Commit to database
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/preferences', methods=['GET', 'PUT'])
@jwt_required()
def user_preferences():
    """Get or update user preferences"""
    try:
        user_id = int(get_jwt_identity())
        
        if request.method == 'GET':
            preferences = UserPreference.query.filter_by(user_id=user_id).first()
            if not preferences:
                # Create default preferences
                preferences = UserPreference(user_id=user_id)
                db.session.add(preferences)
                db.session.commit()
            
            return jsonify({'preferences': preferences.to_dict()}), 200
        
        else:  # PUT
            data = request.get_json()
            preferences = UserPreference.query.filter_by(user_id=user_id).first()
            
            if not preferences:
                preferences = UserPreference(user_id=user_id)
                db.session.add(preferences)
            
            # Update fields
            if 'currency' in data:
                preferences.currency = data['currency']
            if 'notification_enabled' in data:
                preferences.notification_enabled = data['notification_enabled']
            if 'risk_alert_threshold' in data:
                preferences.risk_alert_threshold = data['risk_alert_threshold']
            if 'theme' in data:
                preferences.theme = data['theme']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Preferences updated successfully',
                'preferences': preferences.to_dict()
            }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
