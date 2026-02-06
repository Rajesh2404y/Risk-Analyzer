"""
Manual Email Alert Trigger
Run this to send yourself a financial alert email
Usage: python send_alert.py YOUR_EMAIL
"""
import sys
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.email_service import email_service

def send_test_alert(user_email: str):
    """Send a test financial alert"""
    
    print("=" * 60)
    print("📧 Sending Financial Alert Email")
    print("=" * 60)
    
    # Check configuration
    if not email_service.is_configured():
        print("❌ Email service not configured!")
        print("Please check your .env file:")
        print("  - SMTP_USER")
        print("  - SMTP_PASSWORD")
        return False
    
    print(f"✓ Email configured")
    print(f"✓ Sending to: {user_email}")
    print()
    
    # Sample recommendations
    recommendations = [
        {
            'type': 'critical_alert',
            'title': '🚨 Critical: Low Savings Rate Detected',
            'message': 'Your savings rate is 8.5%. AI analysis shows you are spending $4,200 against income of $4,600. Immediate action required.',
            'impact': 'Risk of financial instability. Recommended savings rate: 20%+',
            'priority': 9
        },
        {
            'type': 'expense_reduction',
            'title': '💰 Reduce Monthly Expenses',
            'message': 'AI recommends cutting non-essential spending by 15-20% to improve financial health.',
            'impact': 'Could save $630 per month',
            'priority': 8
        },
        {
            'type': 'emergency_fund',
            'title': '🏦 Build Emergency Fund',
            'message': 'AI recommends maintaining 6 months of expenses as emergency savings.',
            'impact': 'Target: $25,200',
            'priority': 7
        }
    ]
    
    # Send email
    print("📤 Sending email...")
    success = email_service.send_recommendation_alert(
        user_email=user_email,
        user_name="Test User",
        recommendations=recommendations
    )
    
    if success:
        print()
        print("=" * 60)
        print("✅ SUCCESS! Email sent successfully")
        print("=" * 60)
        print(f"Check your inbox: {user_email}")
        print("(Also check spam folder)")
        print()
        return True
    else:
        print()
        print("=" * 60)
        print("❌ FAILED to send email")
        print("=" * 60)
        print("Possible issues:")
        print("  1. Wrong Gmail App Password")
        print("  2. 2FA not enabled on Gmail")
        print("  3. Network/firewall blocking SMTP")
        print()
        print("Try running: python test_email.py")
        print("For detailed error messages")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        email = os.getenv('SMTP_USER')
        if not email:
            print("Error: No email provided and SMTP_USER not set in .env")
            print("Usage: python send_alert.py YOUR_EMAIL")
            sys.exit(1)
        print(f"No email provided, using SMTP_USER: {email}")
    else:
        email = sys.argv[1]
    
    send_test_alert(email)
