"""
Test SMS Service
Run: python test_sms.py +919876543210
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.sms_service import sms_service

def test_sms(phone_number=None):
    """Test SMS sending"""
    
    print("=" * 60)
    print("📱 SMS SERVICE TEST")
    print("=" * 60)
    print()
    
    # Check configuration
    print("Configuration:")
    print(f"  Account SID: {os.getenv('TWILIO_ACCOUNT_SID', 'NOT SET')[:10]}...")
    print(f"  Auth Token: {'SET' if os.getenv('TWILIO_AUTH_TOKEN') else 'NOT SET'}")
    print(f"  From Number: {os.getenv('TWILIO_PHONE_NUMBER', 'NOT SET')}")
    print()
    
    if not sms_service.is_configured():
        print("❌ SMS service not configured!")
        print()
        print("Setup required:")
        print("  1. Sign up: https://www.twilio.com/try-twilio")
        print("  2. Get Account SID, Auth Token, Phone Number")
        print("  3. Add to backend/.env:")
        print("     TWILIO_ACCOUNT_SID=ACxxxxx...")
        print("     TWILIO_AUTH_TOKEN=your_token")
        print("     TWILIO_PHONE_NUMBER=+1234567890")
        print()
        print("See SMS_SETUP_GUIDE.md for detailed instructions")
        return False
    
    print("✅ SMS service configured")
    print()
    
    # Get phone number
    if not phone_number:
        if len(sys.argv) > 1:
            phone_number = sys.argv[1]
        else:
            phone_number = input("Enter phone number (with country code, e.g., +919876543210): ").strip()
    
    if not phone_number:
        print("❌ Phone number required")
        return False
    
    # Ensure country code
    if not phone_number.startswith('+'):
        print(f"⚠️  Adding +91 (India) country code")
        phone_number = '+91' + phone_number
    
    print(f"📤 Sending test SMS to: {phone_number}")
    print()
    
    # Test message
    message = """🧪 Test Alert - Risk Analyzer

Your SMS alerts are working!

You'll receive financial alerts when:
• Savings rate is low
• Budget exceeded
• High-risk detected

Dashboard: http://localhost:5173"""
    
    # Send SMS
    success = sms_service.send_sms(phone_number, message)
    
    print()
    print("=" * 60)
    
    if success:
        print("✅ SUCCESS! SMS sent")
        print()
        print(f"Check your phone: {phone_number}")
        print()
        print("If not received:")
        print("  • Check Twilio console: https://console.twilio.com/logs")
        print("  • Verify phone number format")
        print("  • Check trial account restrictions")
    else:
        print("❌ FAILED to send SMS")
        print()
        print("Common issues:")
        print("  • Wrong Twilio credentials")
        print("  • Invalid phone number format")
        print("  • Trial account restrictions")
        print("  • Insufficient Twilio balance")
        print()
        print("Check Twilio console for details:")
        print("  https://console.twilio.com/logs")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    test_sms()
