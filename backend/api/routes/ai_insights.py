"""
AI Insights API Routes
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ml.ai_insights import ai_insights

ai_insights_bp = Blueprint('ai_insights', __name__)


@ai_insights_bp.route('/transaction-analysis', methods=['GET'])
@jwt_required()
def transaction_analysis():
    """Get AI-powered transaction analysis"""
    try:
        user_id = int(get_jwt_identity())
        result = ai_insights.get_transaction_analysis(user_id)
        return jsonify({
            'type': 'transaction_analysis',
            'title': 'Transaction Analysis',
            'description': 'Key trends, patterns, and performance insights',
            **result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_insights_bp.route('/anomaly-detection', methods=['GET'])
@jwt_required()
def anomaly_detection():
    """Get AI-powered anomaly detection"""
    try:
        user_id = int(get_jwt_identity())
        result = ai_insights.get_anomaly_explanation(user_id)
        return jsonify({
            'type': 'anomaly_detection',
            'title': 'Anomaly Detection',
            'description': 'Unusual patterns and their explanations',
            **result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_insights_bp.route('/forecast-comparison', methods=['GET'])
@jwt_required()
def forecast_comparison():
    """Get AI-powered forecast vs actual comparison"""
    try:
        user_id = int(get_jwt_identity())
        result = ai_insights.get_forecast_comparison(user_id)
        return jsonify({
            'type': 'forecast_comparison',
            'title': 'Forecast vs Actual',
            'description': 'Compare predictions with actual performance',
            **result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_insights_bp.route('/seasonality', methods=['GET'])
@jwt_required()
def seasonality_analysis():
    """Get AI-powered seasonality analysis"""
    try:
        user_id = int(get_jwt_identity())
        result = ai_insights.get_seasonality_analysis(user_id)
        return jsonify({
            'type': 'seasonality',
            'title': 'Seasonality Patterns',
            'description': 'Recurring trends and seasonal impacts',
            **result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_insights_bp.route('/executive-summary', methods=['GET'])
@jwt_required()
def executive_summary():
    """Get AI-powered executive summary"""
    try:
        user_id = int(get_jwt_identity())
        result = ai_insights.get_executive_summary(user_id)
        return jsonify({
            'type': 'executive_summary',
            'title': 'Executive Summary',
            'description': 'Management-level overview and recommendations',
            **result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_insights_bp.route('/data-quality', methods=['GET'])
@jwt_required()
def data_quality():
    """Get AI-powered data quality assessment"""
    try:
        user_id = int(get_jwt_identity())
        result = ai_insights.get_data_quality_assessment(user_id)
        return jsonify({
            'type': 'data_quality',
            'title': 'Data Quality Assessment',
            'description': 'Reliability and accuracy evaluation',
            **result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_insights_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def action_recommendations():
    """Get AI-powered action recommendations"""
    try:
        user_id = int(get_jwt_identity())
        result = ai_insights.get_action_recommendations(user_id)
        return jsonify({
            'type': 'recommendations',
            'title': 'Action Recommendations',
            'description': 'Actionable steps to improve performance',
            **result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ai_insights_bp.route('/all', methods=['GET'])
@jwt_required()
def all_insights():
    """Get all AI insights at once"""
    try:
        user_id = int(get_jwt_identity())
        
        insights = {
            'executive_summary': ai_insights.get_executive_summary(user_id),
            'transaction_analysis': ai_insights.get_transaction_analysis(user_id),
            'anomaly_detection': ai_insights.get_anomaly_explanation(user_id),
            'recommendations': ai_insights.get_action_recommendations(user_id)
        }
        
        return jsonify({
            'insights': insights,
            'count': len(insights)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
