"""
Add SMS alert fields to user_preferences table
Run: python add_sms_fields.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.models import db
from app import app

def add_sms_fields():
    """Add phone_number and sms_alerts_enabled columns"""
    
    print("=" * 60)
    print("Adding SMS Alert Fields to Database")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Check if columns exist
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('user_preferences')]
            
            print(f"\nCurrent columns: {columns}")
            
            # Add phone_number if not exists
            if 'phone_number' not in columns:
                print("\n✓ Adding phone_number column...")
                db.session.execute(text(
                    "ALTER TABLE user_preferences ADD COLUMN phone_number VARCHAR(20)"
                ))
                print("  ✅ phone_number added")
            else:
                print("\n✓ phone_number column already exists")
            
            # Add sms_alerts_enabled if not exists
            if 'sms_alerts_enabled' not in columns:
                print("\n✓ Adding sms_alerts_enabled column...")
                db.session.execute(text(
                    "ALTER TABLE user_preferences ADD COLUMN sms_alerts_enabled BOOLEAN DEFAULT FALSE"
                ))
                print("  ✅ sms_alerts_enabled added")
            else:
                print("\n✓ sms_alerts_enabled column already exists")
            
            db.session.commit()
            
            print("\n" + "=" * 60)
            print("✅ SUCCESS! SMS fields added to database")
            print("=" * 60)
            print("\nYou can now:")
            print("  1. Set up Twilio account")
            print("  2. Add phone number in user preferences")
            print("  3. Receive SMS alerts!")
            print()
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {e}")
            print("\nIf columns already exist, this is normal.")

if __name__ == "__main__":
    add_sms_fields()
