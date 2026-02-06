"""
Quick test script to verify email configuration
Run: python test_email.py
"""
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

def test_email():
    """Test email sending"""
    
    # Get config
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    
    print("=" * 50)
    print("Email Configuration Test")
    print("=" * 50)
    print(f"SMTP Host: {smtp_host}")
    print(f"SMTP Port: {smtp_port}")
    print(f"SMTP User: {smtp_user}")
    print(f"From Email: {from_email}")
    print(f"Password Set: {'Yes' if smtp_password else 'No'}")
    print("=" * 50)
    
    if not smtp_user or not smtp_password:
        print("❌ ERROR: SMTP credentials not configured!")
        return False
    
    try:
        # Create test message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🧪 Test Email - Risk Analyzer"
        msg['From'] = from_email
        msg['To'] = smtp_user  # Send to yourself
        
        html = """
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #1976d2;">✅ Email Configuration Successful!</h2>
            <p>Your Risk Analyzer email alerts are working correctly.</p>
            <p>You will now receive AI-powered financial recommendations.</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Connect and send
        print("\n📧 Connecting to SMTP server...")
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            print("🔐 Starting TLS...")
            server.starttls()
            
            print("🔑 Authenticating...")
            server.login(smtp_user, smtp_password)
            
            print("📤 Sending email...")
            server.sendmail(from_email, smtp_user, msg.as_string())
        
        print(f"\n✅ SUCCESS! Test email sent to {smtp_user}")
        print("Check your inbox (and spam folder)")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ Authentication Failed: {e}")
        print("Check your Gmail App Password is correct")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_email()
