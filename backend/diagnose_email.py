"""
Complete Email Diagnostic Tool
Tests your exact configuration and shows what's wrong
"""
import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

def diagnose():
    print("\n" + "=" * 70)
    print("🔍 EMAIL CONFIGURATION DIAGNOSTIC")
    print("=" * 70 + "\n")
    
    # Get config
    host = os.getenv('SMTP_HOST')
    port = os.getenv('SMTP_PORT')
    user = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASSWORD')
    
    print("📋 Current Configuration:")
    print("-" * 70)
    print(f"SMTP_HOST: {host}")
    print(f"SMTP_PORT: {port}")
    print(f"SMTP_USER: {user}")
    print(f"SMTP_PASSWORD: {password[:4]}{'*' * 8}{password[-4:] if len(password) > 8 else ''} ({len(password)} chars)")
    print()
    
    # Check each component
    issues = []
    
    print("🔍 Checking Configuration...")
    print("-" * 70)
    
    # Check 1: Host
    if host != 'smtp.gmail.com':
        print("❌ SMTP_HOST is wrong")
        issues.append("host")
    else:
        print("✅ SMTP_HOST is correct")
    
    # Check 2: Port
    if port != '587':
        print("❌ SMTP_PORT is wrong")
        issues.append("port")
    else:
        print("✅ SMTP_PORT is correct")
    
    # Check 3: User
    if not user or '@gmail.com' not in user:
        print("❌ SMTP_USER is invalid")
        issues.append("user")
    else:
        print(f"✅ SMTP_USER is valid: {user}")
    
    # Check 4: Password
    if not password:
        print("❌ SMTP_PASSWORD is empty")
        issues.append("password_empty")
    elif len(password) != 16:
        print(f"⚠️  SMTP_PASSWORD length is {len(password)} (should be 16)")
        issues.append("password_length")
    elif ' ' in password:
        print("❌ SMTP_PASSWORD contains spaces")
        issues.append("password_spaces")
    else:
        print(f"✅ SMTP_PASSWORD format looks correct (16 chars)")
    
    print()
    
    # Test connection
    if not issues or issues == ['password_length']:
        print("🔌 Testing SMTP Connection...")
        print("-" * 70)
        
        try:
            print("1. Connecting to smtp.gmail.com:587...")
            server = smtplib.SMTP(host, int(port), timeout=10)
            print("   ✅ Connected")
            
            print("2. Starting TLS encryption...")
            server.starttls()
            print("   ✅ TLS started")
            
            print("3. Attempting login...")
            server.login(user, password)
            print("   ✅ LOGIN SUCCESSFUL!")
            
            server.quit()
            
            print()
            print("=" * 70)
            print("🎉 SUCCESS! Your email configuration works!")
            print("=" * 70)
            print("\nYou can now send emails. Run: python test_email.py")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"   ❌ AUTHENTICATION FAILED")
            print()
            print("=" * 70)
            print("🚨 PROBLEM IDENTIFIED: Gmail Rejected Your Password")
            print("=" * 70)
            print()
            print("The password 'vndccdmfmtpvesgt' is NOT VALID.")
            print()
            print("This means:")
            print("  • Password was revoked by Google")
            print("  • Password expired")
            print("  • Password is for a different account")
            print("  • Password was never valid")
            print()
            print("=" * 70)
            print("✅ SOLUTION: Generate New App Password")
            print("=" * 70)
            print()
            print("Step 1: Open this link:")
            print("  👉 https://myaccount.google.com/apppasswords")
            print()
            print(f"Step 2: Sign in with: {user}")
            print()
            print("Step 3: Generate new password:")
            print("  - Select app: Mail")
            print("  - Select device: Windows Computer")
            print("  - Click Generate")
            print("  - Copy the 16-character password")
            print()
            print("Step 4: Update backend\\.env file:")
            print("  - Find: SMTP_PASSWORD=vndccdmfmtpvesgt")
            print("  - Replace with: SMTP_PASSWORD=yournewpassword")
            print("  - Save file")
            print()
            print("Step 5: Run this script again to verify")
            print()
            print("=" * 70)
            print()
            print("⚠️  If you don't see 'App passwords' option:")
            print("   1. Go to: https://myaccount.google.com/security")
            print("   2. Enable '2-Step Verification'")
            print("   3. Then try app passwords again")
            print()
            return False
            
        except smtplib.SMTPConnectError as e:
            print(f"   ❌ CONNECTION FAILED: {e}")
            print("\n   Check your internet connection or firewall")
            return False
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            return False
    else:
        print("=" * 70)
        print("❌ Configuration has errors. Fix them first:")
        print("=" * 70)
        for issue in issues:
            if issue == "host":
                print("  • Set SMTP_HOST=smtp.gmail.com")
            elif issue == "port":
                print("  • Set SMTP_PORT=587")
            elif issue == "user":
                print("  • Set SMTP_USER to your Gmail address")
            elif issue == "password_empty":
                print("  • Set SMTP_PASSWORD to your 16-char app password")
            elif issue == "password_spaces":
                print("  • Remove spaces from SMTP_PASSWORD")
        print()
        return False

if __name__ == "__main__":
    diagnose()
