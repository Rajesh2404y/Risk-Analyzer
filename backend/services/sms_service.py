"""
SMS Service for sending alerts via Twilio
"""
import os
from typing import List, Dict, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class SMSService:
    """SMS service for sending notifications via Twilio"""
    
    def __init__(self):
        """Initialize SMS service with Twilio configuration"""
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER', '')
        self.client = None
        
        if self.is_configured():
            self.client = Client(self.account_sid, self.auth_token)
    
    def is_configured(self) -> bool:
        """Check if SMS service is properly configured"""
        return bool(
            self.account_sid and 
            self.auth_token and 
            self.from_number and
            self.account_sid != 'your-twilio-account-sid' and
            self.auth_token != 'your-twilio-auth-token'
        )
    
    def send_sms(self, to_number: str, message: str) -> bool:
        """
        Send an SMS message
        
        Args:
            to_number: Recipient phone number (format: +1234567890)
            message: SMS message content (max 1600 chars)
        
        Returns:
            bool: True if SMS was sent successfully
        """
        if not self.is_configured():
            print("SMS service not configured. Set TWILIO credentials in .env")
            return False
        
        try:
            # Ensure phone number has country code
            if not to_number.startswith('+'):
                to_number = '+91' + to_number  # Default to India
            
            # Truncate message if too long
            if len(message) > 1600:
                message = message[:1597] + '...'
            
            # Send SMS
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            print(f"SMS sent successfully to {to_number}. SID: {message_obj.sid}")
            return True
            
        except TwilioRestException as e:
            print(f"Twilio Error: {e}")
            return False
        except Exception as e:
            print(f"Failed to send SMS: {e}")
            return False
    
    def send_recommendation_alert(
        self,
        phone_number: str,
        user_name: str,
        recommendations: List[Dict]
    ) -> bool:
        """
        Send AI recommendation alert via SMS
        
        Args:
            phone_number: User's phone number
            user_name: User's name for personalization
            recommendations: List of recommendation dictionaries
        
        Returns:
            bool: True if SMS was sent successfully
        """
        if not recommendations:
            return False
        
        # Filter high-priority recommendations
        high_priority = [r for r in recommendations if r.get('priority', 0) >= 7]
        
        if not high_priority:
            return False
        
        # Build SMS message (keep it short)
        message = f"🚨 Financial Alert for {user_name}\n\n"
        
        for i, rec in enumerate(high_priority[:3], 1):  # Max 3 recommendations
            message += f"{i}. {rec.get('title', 'Alert')}\n"
            message += f"   {rec.get('message', '')[:80]}...\n\n"
        
        message += "Check dashboard for details: http://localhost:5173"
        
        return self.send_sms(phone_number, message)


# Global instance
sms_service = SMSService()
