# 📧 Email Alerts - Final Setup

## 🎯 Your Goal
Get email alerts working for financial notifications.

## ⚠️ Current Issue
Your Gmail app password is **rejected**. You need a new one.

## ✅ Solution (3 Steps)

### Step 1: Generate Gmail App Password

1. **Open**: https://myaccount.google.com/apppasswords
2. **Sign in**: rajeshyuvaraja24@gmail.com
3. **Select**:
   - App: **Mail**
   - Device: **Windows Computer**
4. **Click**: Generate
5. **Copy**: The 16-character password (like: `abcd efgh ijkl mnop`)

**Important**: Remove all spaces! Use: `abcdefghijklmnop`

### Step 2: Update .env File

Open `backend\.env` and update line 21:

```env
SMTP_PASSWORD=abcdefghijklmnop
```

Replace `abcdefghijklmnop` with your actual 16-character password (no spaces).

### Step 3: Test

```bash
cd backend
python diagnose_email.py
```

If successful, you'll see:
```
✅ LOGIN SUCCESSFUL!
🎉 SUCCESS! Your email configuration works!
```

## 🚨 If You Don't See "App Passwords"

You need to enable 2-Factor Authentication first:

1. Go to: https://myaccount.google.com/security
2. Click **2-Step Verification**
3. Follow the setup
4. Then try Step 1 again

## 🧪 Test Email Sending

After updating password:

```bash
# Test configuration
python diagnose_email.py

# Send test email
python test_email.py

# Send full alert
python send_alert.py
```

## 📧 What You'll Receive

Beautiful HTML emails with:
- 🚨 Risk level and score
- 💰 Financial analysis
- 📊 Personalized recommendations
- 🔗 Dashboard link

## 🔧 Current Configuration

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=rajeshyuvaraja24@gmail.com
SMTP_PASSWORD=your-app-password-here  ← UPDATE THIS
FROM_EMAIL=rajeshyuvaraja24@gmail.com
FROM_NAME=AI Expense Risk Analyzer
```

## ✅ Checklist

- [ ] Go to https://myaccount.google.com/apppasswords
- [ ] Generate new 16-character password
- [ ] Copy password (remove spaces)
- [ ] Update `backend\.env` file
- [ ] Save file
- [ ] Run `python diagnose_email.py`
- [ ] See success message!

## 🎬 Quick Commands

```bash
cd backend

# Check configuration
python diagnose_email.py

# Test email
python test_email.py

# Send alert
python send_alert.py
```

---

**The password in your .env is invalid. Generate a new one now!** 🔑

Link: https://myaccount.google.com/apppasswords
