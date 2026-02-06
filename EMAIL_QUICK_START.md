# 📧 Email Alert Quick Start

## ✅ What's Already Done

Your email alerts are **fully configured and ready to use**!

- ✓ Gmail SMTP configured
- ✓ App password set
- ✓ Email service implemented
- ✓ AI-powered recommendations ready
- ✓ Frontend button added
- ✓ Test scripts created

## 🚀 3 Ways to Test (Pick One)

### Option 1: Easiest - Test Script
```bash
cd backend
python test_email.py
```
**Result**: Sends simple test email to verify configuration

### Option 2: With Sample Data
```bash
cd backend
python send_alert.py
```
**Result**: Sends realistic financial alert with sample recommendations

### Option 3: Via Web UI
1. Start servers: `python app.py` (backend) + `npm run dev` (frontend)
2. Login at `http://localhost:5173`
3. Go to **AI Insights** page
4. Click **"Send Email Alert"** button (top-right)

**Result**: Sends alert based on your actual transaction data

## 📧 What You'll Receive

Beautiful HTML email with:
- 🎯 Your risk score and level
- 💰 Income vs expenses analysis
- 📊 Savings rate calculation
- 🚨 Personalized recommendations
- 🔗 Link to dashboard

## ⚠️ Important Notes

1. **Need Transactions First**: Add some transactions before testing via UI (Option 3)
2. **Check Spam**: First email might go to spam folder
3. **Gmail Only**: Currently configured for Gmail (can change in .env)

## 🔧 If Email Doesn't Arrive

```bash
# Run diagnostic test
cd backend
python test_email.py
```

Common fixes:
- Regenerate Gmail App Password: https://myaccount.google.com/apppasswords
- Enable 2FA on Gmail account
- Check `.env` has: `SMTP_PASSWORD=vndccdmfmtpvesgt` (no spaces)

## 📝 Your Configuration

```
Email: rajeshyuvaraja24@gmail.com
SMTP: Gmail (smtp.gmail.com:587)
Status: ✅ Ready
```

## 🎯 Next Steps

1. **Test Now**: Run `python test_email.py`
2. **Check Email**: Look in inbox (and spam)
3. **Add Transactions**: Add real data for meaningful alerts
4. **Use UI Button**: Try the web interface

---

**Everything is ready! Just run the test script.** 🚀
