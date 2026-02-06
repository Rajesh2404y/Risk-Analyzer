# Email Alert Implementation Guide

## ✅ Current Status
Your email configuration is already set up! Here's what's configured:

- **Email**: rajeshyuvaraja24@gmail.com
- **SMTP**: Gmail (smtp.gmail.com:587)
- **App Password**: Configured ✓

## 🚀 How to Test Email Alerts

### Method 1: Quick Test Script (Recommended)
```bash
cd backend
python test_email.py
```

This will:
- Verify your SMTP configuration
- Send a test email to yourself
- Show detailed error messages if something fails

### Method 2: Via Frontend UI
1. Start both servers:
   ```bash
   # Terminal 1 - Backend
   cd backend
   python app.py

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. Open browser: `http://localhost:5173`

3. Login to your account

4. Go to **AI Insights** page

5. Click the **"Send Email Alert"** button in the top-right

6. Check your email inbox (and spam folder)

### Method 3: API Test (Advanced)
```bash
# Get your JWT token first by logging in
curl -X POST http://localhost:5000/api/recommendations/test-email \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

## 📧 What Emails Will You Receive?

The system sends AI-powered financial alerts when:

1. **Low Savings Rate** (< 10%)
   - Critical alert with immediate action required
   - Expense reduction recommendations

2. **Moderate Risk** (10-20% savings)
   - Warning about financial health
   - Optimization suggestions

3. **Budget Alerts**
   - When approaching category limits
   - Overspending notifications

4. **Emergency Fund Recommendations**
   - Suggestions to build 6-month emergency fund

## 🎯 Email Content

Each alert includes:
- 🚨 Risk level and score
- 💰 Financial analysis (income, expenses, savings rate)
- 📊 Personalized recommendations
- 🔗 Direct link to your dashboard
- ⏰ Timestamp of analysis

## 🔧 Troubleshooting

### If emails don't arrive:

1. **Check Gmail App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Generate new 16-character password
   - Update `.env` file: `SMTP_PASSWORD=your-new-password`
   - Remove all spaces from password

2. **Check Spam Folder**
   - Gmail might filter automated emails
   - Mark as "Not Spam" if found

3. **Verify 2FA is Enabled**
   - App passwords only work with 2FA enabled
   - Enable at: https://myaccount.google.com/security

4. **Check Backend Console**
   - Look for error messages when sending
   - Common errors:
     - `SMTPAuthenticationError` = Wrong password
     - `SMTPConnectError` = Network/firewall issue
     - `Connection refused` = Wrong SMTP host/port

5. **Test with Script**
   ```bash
   cd backend
   python test_email.py
   ```
   This shows detailed error messages

## 📝 Current Configuration

Your `.env` file has:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=rajeshyuvaraja24@gmail.com
SMTP_PASSWORD=vndccdmfmtpvesgt
FROM_EMAIL=rajeshyuvaraja24@gmail.com
FROM_NAME=AI Expense Risk Analyzer
```

## 🎨 Customizing Email Alerts

### Change Email Frequency
Edit `backend/api/routes/recommendations.py`:
```python
# Only send if there are high-priority recommendations
high_priority = [r for r in recommendations if r.get('priority', 0) >= 7]
```
Change `>= 7` to `>= 5` for more frequent alerts

### Change Risk Thresholds
Edit the risk calculation:
```python
if savings_rate < 10:  # Change this threshold
    risk_score = 80
```

### Customize Email Template
Edit `backend/services/email_service.py`:
- Modify `_build_recommendation_email_html()` for HTML design
- Modify `_build_recommendation_email_text()` for plain text

## 🔄 Automated Alerts (Future Enhancement)

To send alerts automatically:

1. **Add Scheduler** (install: `pip install apscheduler`)
2. **Create Cron Job** in `backend/app.py`:
   ```python
   from apscheduler.schedulers.background import BackgroundScheduler
   
   def send_daily_alerts():
       # Send alerts to all users
       pass
   
   scheduler = BackgroundScheduler()
   scheduler.add_job(send_daily_alerts, 'cron', hour=9)  # 9 AM daily
   scheduler.start()
   ```

## ✅ Next Steps

1. **Add Transactions** - You need transaction data for meaningful alerts
2. **Test Email** - Run `python test_email.py`
3. **Check Inbox** - Look for test email
4. **Use UI Button** - Try the "Send Email Alert" button in AI Insights page
5. **Monitor Logs** - Watch backend console for any errors

## 📞 Support

If you encounter issues:
1. Run `python test_email.py` and share the output
2. Check backend console logs
3. Verify Gmail settings at https://myaccount.google.com/security

---

**Your email alerts are ready to use! 🎉**
