# 🔑 Fix Gmail Authentication Error

## ❌ Current Problem
```
SMTP Authentication failed: Username and Password not accepted
```

Your Gmail app password is **invalid or expired**.

## ✅ Solution: Generate New App Password

### Step 1: Enable 2-Factor Authentication (if not already)
1. Go to: https://myaccount.google.com/security
2. Click **2-Step Verification**
3. Follow the setup process
4. **You MUST have 2FA enabled to create app passwords**

### Step 2: Generate App Password
1. Go to: **https://myaccount.google.com/apppasswords**
2. Sign in if prompted
3. In "Select app" dropdown: Choose **Mail**
4. In "Select device" dropdown: Choose **Windows Computer** (or Other)
5. Click **Generate**
6. Google will show a **16-character password** like: `abcd efgh ijkl mnop`

### Step 3: Update Your .env File
1. Open: `backend/.env`
2. Copy the 16-character password (remove spaces)
3. Update this line:
   ```env
   SMTP_PASSWORD=abcdefghijklmnop
   ```
   (Replace with your actual password, NO SPACES)

### Step 4: Test
```bash
cd backend
python test_email.py
```

## 📋 Quick Checklist

- [ ] 2FA enabled on Gmail account
- [ ] Generated new app password at https://myaccount.google.com/apppasswords
- [ ] Copied 16-character password (removed spaces)
- [ ] Updated `backend/.env` file
- [ ] Saved the file
- [ ] Ran `python test_email.py`

## 🎯 Example .env Configuration

```env
# Correct format (no spaces in password)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=rajeshyuvaraja24@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
FROM_EMAIL=rajeshyuvaraja24@gmail.com
FROM_NAME=AI Expense Risk Analyzer
```

## ⚠️ Common Mistakes

1. **Spaces in password**: `abcd efgh ijkl mnop` ❌
   - Should be: `abcdefghijklmnop` ✅

2. **Using Gmail account password**: Regular password doesn't work ❌
   - Must use app password ✅

3. **2FA not enabled**: App passwords require 2FA ❌
   - Enable 2FA first ✅

4. **Wrong email**: Using different email than configured ❌
   - Use: rajeshyuvaraja24@gmail.com ✅

## 🔗 Direct Links

- **Generate App Password**: https://myaccount.google.com/apppasswords
- **Enable 2FA**: https://myaccount.google.com/security
- **Gmail Security Settings**: https://myaccount.google.com/security

## 📞 Still Not Working?

If you still get authentication errors after generating new app password:

1. **Wait 5 minutes** - New passwords take time to activate
2. **Try different app name** - Generate another password with different name
3. **Check account security** - Gmail might have blocked "less secure" access
4. **Use different email** - Try with another Gmail account

## 🎬 Next Steps

1. Go to: https://myaccount.google.com/apppasswords
2. Generate new 16-character password
3. Update `backend/.env` with password (no spaces)
4. Run: `python test_email.py`
5. Check your email inbox!

---

**The current password `vndccdmfmtpvesgt` is not working. You need to generate a fresh one.** 🔑
