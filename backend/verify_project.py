"""
Final Project Verification Script
Checks all critical components before deployment
"""
import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[MISSING] {description}: {filepath}")
        return False

def check_env_config():
    """Check .env configuration"""
    print("\n" + "="*60)
    print("CHECKING ENVIRONMENT CONFIGURATION")
    print("="*60)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        'SECRET_KEY': 'Flask secret key',
        'JWT_SECRET_KEY': 'JWT secret key',
        'DATABASE_URL': 'Database connection',
        'SMTP_HOST': 'Email SMTP host',
        'SMTP_PORT': 'Email SMTP port',
        'SMTP_USER': 'Email user',
        'SMTP_PASSWORD': 'Email password',
    }
    
    all_set = True
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value and value not in ['your-secret-key-here', 'your-jwt-secret-key-here', 'your-app-password-here']:
            if var == 'SMTP_PASSWORD':
                print(f"[OK] {desc}: {value[:4]}***")
            else:
                print(f"[OK] {desc}: {value[:30]}...")
        else:
            print(f"[NOT SET] {desc}")
            all_set = False
    
    return all_set

def check_python_syntax():
    """Check Python files for syntax errors"""
    print("\n" + "="*60)
    print("CHECKING PYTHON SYNTAX")
    print("="*60)
    
    files_to_check = [
        'app.py',
        'ml/risk_calculator.py',
        'api/routes/recommendations.py',
        'api/routes/categories.py',
        'services/email_service.py',
        'database/models.py',
    ]
    
    all_valid = True
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                compile(f.read(), filepath, 'exec')
            print(f"[OK] {filepath}")
        except SyntaxError as e:
            print(f"[ERROR] {filepath}: {e}")
            all_valid = False
        except FileNotFoundError:
            print(f"[NOT FOUND] {filepath}")
            all_valid = False
    
    return all_valid

def check_imports():
    """Check if all required packages are installed"""
    print("\n" + "="*60)
    print("CHECKING REQUIRED PACKAGES")
    print("="*60)
    
    required_packages = [
        ('flask', 'flask'),
        ('flask_cors', 'flask_cors'),
        ('flask_jwt_extended', 'flask_jwt_extended'),
        ('sqlalchemy', 'sqlalchemy'),
        ('pymysql', 'pymysql'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('sklearn', 'scikit-learn'),
        ('bcrypt', 'bcrypt'),
        ('dotenv', 'python-dotenv'),
    ]
    
    all_installed = True
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"[OK] {package_name}")
        except ImportError:
            print(f"[NOT INSTALLED] {package_name}")
            all_installed = False
    
    return all_installed

def check_critical_files():
    """Check if all critical files exist"""
    print("\n" + "="*60)
    print("CHECKING CRITICAL FILES")
    print("="*60)
    
    critical_files = [
        ('.env', 'Environment configuration'),
        ('app.py', 'Main application'),
        ('requirements.txt', 'Python dependencies'),
        ('database/models.py', 'Database models'),
        ('ml/risk_calculator.py', 'Risk calculator'),
        ('services/email_service.py', 'Email service'),
    ]
    
    all_exist = True
    for filepath, desc in critical_files:
        if not check_file_exists(filepath, desc):
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("RISK ANALYZER - FINAL VERIFICATION")
    print("="*60)
    
    # Change to backend directory
    os.chdir(Path(__file__).parent)
    
    results = {
        'Files': check_critical_files(),
        'Environment': check_env_config(),
        'Python Syntax': check_python_syntax(),
        'Packages': check_imports(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    for check, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{check}: {status}")
    
    print("\n" + "="*60)
    
    if all(results.values()):
        print("ALL CHECKS PASSED! Project is ready to deploy.")
        print("="*60)
        print("\nNext steps:")
        print("1. Test email: python test_email.py")
        print("2. Start backend: python app.py")
        print("3. Start frontend: cd ../frontend && npm run dev")
        print("4. Push to GitHub: git add . && git commit -m 'Ready' && git push")
        return 0
    else:
        print("[WARNING] SOME CHECKS FAILED! Fix issues before deploying.")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
