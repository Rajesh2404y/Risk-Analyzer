"""
Interactive Email Password Updater
This will help you update your Gmail app password
"""
import os
import re

def update_password():
    from dotenv import load_dotenv
    load_dotenv()
    
    current_email = os.getenv('SMTP_USER', 'your-email@gmail.com')
    
    print("=" * 70)
    print("🔑 GMAIL APP PASSWORD UPDATER")
    print("=" * 70)
    print()
    print(f"Current email: {current_email}")
    print()
    print("=" * 70)
    print()
    
    print("📋 STEP 1: Generate New App Password")
    print("-" * 70)
    print("1. Open this link in your browser:")
    print("   👉 https://myaccount.google.com/apppasswords")
    print()
    print(f"2. Sign in with: {current_email}")
    print()
    print("3. If you see 'App passwords' page:")
    print("   - Select app: Mail")
    print("   - Select device: Windows Computer")
    print("   - Click 'Generate'")
    print()
    print("4. If you DON'T see 'App passwords':")
    print("   - You need to enable 2-Factor Authentication first")
    print("   - Go to: https://myaccount.google.com/security")
    print("   - Enable '2-Step Verification'")
    print("   - Then try app passwords again")
    print()
    print("5. Copy the 16-character password shown")
    print("   Example: abcd efgh ijkl mnop")
    print()
    print("=" * 70)
    print()
    
    # Get new password
    print("📝 STEP 2: Enter Your New Password")
    print("-" * 70)
    new_password = input("Paste your new 16-character password here: ").strip()
    
    # Remove spaces
    new_password = new_password.replace(' ', '')
    
    if len(new_password) != 16:
        print()
        print(f"⚠️  WARNING: Password length is {len(new_password)} characters")
        print("   Gmail app passwords should be exactly 16 characters")
        print()
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return
    
    print()
    print("=" * 70)
    print()
    
    # Update .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Replace password
        old_pattern = r'SMTP_PASSWORD=.*'
        new_line = f'SMTP_PASSWORD={new_password}'
        
        new_content = re.sub(old_pattern, new_line, content)
        
        # Write back
        with open(env_path, 'w') as f:
            f.write(new_content)
        
        print("✅ SUCCESS! Password updated in .env file")
        print()
        print(f"New password: {new_password[:4]}{'*' * 8}{new_password[-4:]}")
        print()
        print("=" * 70)
        print()
        print("🧪 STEP 3: Test Your Email")
        print("-" * 70)
        print("Run this command to test:")
        print()
        print("   python test_email.py")
        print()
        print("If it works, you'll receive an email at:")
        print(f"   {current_email}")
        print()
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        print("Manual update required:")
        print(f"1. Open: {env_path}")
        print(f"2. Find: SMTP_PASSWORD=vndccdmfmtpvesgt")
        print(f"3. Replace with: SMTP_PASSWORD={new_password}")
        print("4. Save file")

if __name__ == "__main__":
    update_password()
