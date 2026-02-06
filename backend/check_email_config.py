"""
Email Configuration Checker
Shows your current email settings and validates them
"""
import os
from dotenv import load_dotenv

load_dotenv()

def check_config():
    """Check email configuration"""
    
    print("=" * 60)
    print("📧 EMAIL CONFIGURATION CHECK")
    print("=" * 60)
    print()
    
    # Get values
    smtp_host = os.getenv('SMTP_HOST', '')
    smtp_port = os.getenv('SMTP_PORT', '')
    smtp_user = os.getenv('SMTP_USER', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    from_email = os.getenv('FROM_EMAIL', '')
    from_name = os.getenv('FROM_NAME', '')
    
    # Check each setting
    print("1. SMTP Host")
    if smtp_host == 'smtp.gmail.com':
        print(f"   ✅ {smtp_host}")
    else:
        print(f"   ⚠️  {smtp_host} (should be smtp.gmail.com)")
    print()
    
    print("2. SMTP Port")
    if smtp_port == '587':
        print(f"   ✅ {smtp_port}")
    else:
        print(f"   ⚠️  {smtp_port} (should be 587)")
    print()
    
    print("3. SMTP User (Your Email)")
    if smtp_user and '@gmail.com' in smtp_user:
        print(f"   ✅ {smtp_user}")
    else:
        print(f"   ❌ {smtp_user or 'NOT SET'}")
    print()
    
    print("4. SMTP Password (App Password)")
    if not smtp_password:
        print("   ❌ NOT SET")
        print("   → Generate at: https://myaccount.google.com/apppasswords")
    elif len(smtp_password) == 16:
        # Mask password
        masked = smtp_password[:4] + '*' * 8 + smtp_password[-4:]
        print(f"   ✅ {masked} (16 characters)")
    elif ' ' in smtp_password:
        print(f"   ⚠️  Password contains SPACES (length: {len(smtp_password)})")
        print("   → Remove all spaces from password")
    else:
        print(f"   ⚠️  Length: {len(smtp_password)} characters (should be 16)")
        print("   → Generate new password at: https://myaccount.google.com/apppasswords")
    print()
    
    print("5. From Email")
    if from_email:
        print(f"   ✅ {from_email}")
    else:
        print(f"   ⚠️  NOT SET (will use SMTP_USER)")
    print()
    
    print("6. From Name")
    if from_name:
        print(f"   ✅ {from_name}")
    else:
        print(f"   ⚠️  NOT SET")
    print()
    
    # Overall status
    print("=" * 60)
    
    issues = []
    if smtp_host != 'smtp.gmail.com':
        issues.append("Wrong SMTP host")
    if smtp_port != '587':
        issues.append("Wrong SMTP port")
    if not smtp_user or '@gmail.com' not in smtp_user:
        issues.append("Invalid email address")
    if not smtp_password:
        issues.append("Password not set")
    elif len(smtp_password) != 16:
        issues.append("Password wrong length")
    elif ' ' in smtp_password:
        issues.append("Password has spaces")
    
    if not issues:
        print("✅ CONFIGURATION LOOKS GOOD!")
        print()
        print("Next step: Run 'python test_email.py' to test sending")
    else:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        print()
        print("📝 TO FIX:")
        print("   1. Go to: https://myaccount.google.com/apppasswords")
        print("   2. Generate new 16-character password")
        print("   3. Update backend/.env file:")
        print("      SMTP_PASSWORD=your16charpassword")
        print("   4. Save file and run this script again")
    
    print("=" * 60)

if __name__ == "__main__":
    check_config()
