# 🔧 Email Authentication Troubleshooting

## ❌ Current Error
```
SMTP Authentication failed: Username and Password not accepted
```

## ✅ Solution Checklist

### Option 1: Use Interactive Script (Easiest)
```bash
cd backend
python update_email_password.py
```
This will guide you through updating the password step-by-step.

---

### Option 2: Manual Fix

#### Step 1: Check 2FA Status
1. Go to: https://myaccount.google.com/security
2. Look for "2-Step Verification"
3. **Must be ON** (blue toggle)
4. If OFF, click it and enable it

#### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Sign in: **rajeshyuvaraja24@gmail.com**
3. Select app: **Mail**
4. Select device: **Windows Computer**
5. Click **Generate**
6. Copy the 16-character password

#### Step 3: Update .env File
1. Open: `backend\.env`
2. Find line: `SMTP_PASSWORD=vndccdmfmtpvesgt`
3. Replace with: `SMTP_PASSWORD=your16charpassword`
4. **Remove all spaces** from password
5. Save file

#### Step 4: Test
```bash
cd backend
python test_email.py
```

---

## 🚨 Common Issues

### "I don't see App Passwords option"
**Cause**: 2FA not enabled  
**Fix**: Enable 2-Step Verification first at https://myaccount.google.com/security

### "Password still doesn't work"
**Possible causes**:
1. Spaces in password → Remove all spaces
2. Wrong email → Use rajeshyuvaraja24@gmail.com
3. Old password cached → Restart backend server
4. Password not saved → Check .env file was saved

### "Can't enable 2FA"
**Alternative**: Use a different Gmail account that already has 2FA

---

## 📊 Diagnostic Commands

```bash
# Check current configuration
python check_email_config.py

# Test email sending
python test_email.py

# Update password interactively
python update_email_password.py
```

---

## 🎯 Quick Fix (Copy-Paste)

1. **Open browser**: https://myaccount.google.com/apppasswords
2. **Generate password** (16 characters)
3. **Run this**:
   ```bash
   cd backend
   python update_email_password.py
   ```
4. **Paste password** when prompted
5. **Test**: `python test_email.py`

---

## 📞 Still Stuck?

The password `vndccdmfmtpvesgt` is definitely not working. You MUST:
1. Generate a NEW password from Google
2. Update the .env file
3. Test again

**There's no way around this - the current password is invalid.** 🔑
