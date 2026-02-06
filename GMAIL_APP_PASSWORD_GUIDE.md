# 📧 Gmail App Password - Visual Guide

## 🎯 Your Mission
Get a new 16-character password from Gmail to fix the authentication error.

---

## 📍 Step-by-Step Instructions

### STEP 1: Open Gmail Security Settings
```
🌐 Open this link in your browser:
https://myaccount.google.com/apppasswords
```

### STEP 2: Sign In
```
📧 Sign in with: rajeshyuvaraja24@gmail.com
🔑 Use your regular Gmail password
```

### STEP 3: You'll See This Page
```
┌─────────────────────────────────────────┐
│  App passwords                          │
│                                         │
│  Select app:  [Mail ▼]                 │
│  Select device: [Windows Computer ▼]   │
│                                         │
│  [Generate]                             │
└─────────────────────────────────────────┘
```

### STEP 4: Click Generate
```
You'll see a yellow box with:

┌─────────────────────────────────────────┐
│  Your app password for your device      │
│                                         │
│  abcd efgh ijkl mnop                   │
│                                         │
│  [Done]                                 │
└─────────────────────────────────────────┘

⚠️ COPY THIS PASSWORD NOW!
   It won't be shown again.
```

### STEP 5: Remove Spaces
```
What you see:    abcd efgh ijkl mnop
What you need:   abcdefghijklmnop
                 ↑ No spaces!
```

### STEP 6: Update .env File
```
Open: backend\.env

Find this line:
SMTP_PASSWORD=vndccdmfmtpvesgt

Replace with your new password:
SMTP_PASSWORD=abcdefghijklmnop
              ↑ Your actual password here

Save the file!
```

### STEP 7: Test It
```bash
cd backend
python test_email.py
```

### STEP 8: Check Email
```
✅ Look in inbox: rajeshyuvaraja24@gmail.com
📧 Subject: "🧪 Test Email - Risk Analyzer"

If not in inbox, check SPAM folder!
```

---

## 🚨 Troubleshooting

### "I don't see App Passwords option"
**Solution**: Enable 2-Factor Authentication first
1. Go to: https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow setup
4. Then try app passwords again

### "Authentication still fails"
**Checklist**:
- [ ] Copied password correctly (no spaces)
- [ ] Saved .env file
- [ ] Using correct email: rajeshyuvaraja24@gmail.com
- [ ] Waited 2-3 minutes after generating password
- [ ] Restarted backend server

### "Can't access app passwords page"
**Alternative Method**:
1. Gmail Settings → See all settings
2. Accounts and Import
3. Other Google Account settings
4. Security → App passwords

---

## 📝 Quick Reference

| Setting | Value |
|---------|-------|
| Email | rajeshyuvaraja24@gmail.com |
| SMTP Host | smtp.gmail.com |
| SMTP Port | 587 |
| Password | Get from: https://myaccount.google.com/apppasswords |

---

## ✅ Success Looks Like This

```bash
$ python test_email.py

==================================================
Email Configuration Test
==================================================
SMTP Host: smtp.gmail.com
SMTP Port: 587
SMTP User: rajeshyuvaraja24@gmail.com
From Email: rajeshyuvaraja24@gmail.com
Password Set: Yes
==================================================

📧 Connecting to SMTP server...
🔐 Starting TLS...
🔑 Authenticating...
📤 Sending email...

✅ SUCCESS! Test email sent to rajeshyuvaraja24@gmail.com
Check your inbox (and spam folder)
```

---

## 🎯 TL;DR (Too Long; Didn't Read)

1. Go to: https://myaccount.google.com/apppasswords
2. Generate password
3. Copy it (remove spaces)
4. Put in `backend/.env` → `SMTP_PASSWORD=yourpassword`
5. Run: `python test_email.py`
6. Done! 🎉

---

**Current password is expired/invalid. Generate a new one now!** ⚡
