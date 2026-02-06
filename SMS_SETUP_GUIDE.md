# 📱 SMS Alerts Setup Guide

## ✅ What's Implemented

SMS alerts are now fully integrated! You can receive financial alerts via text message.

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Twilio Library
```bash
cd backend
pip install twilio
```

### Step 2: Get Twilio Credentials (FREE)

1. **Sign up**: https://www.twilio.com/try-twilio
   - Free trial includes $15 credit
   - No credit card required initially

2. **Get your credentials**:
   - Go to: https://console.twilio.com
   - Copy **Account SID** (starts with AC...)
   - Copy **Auth Token** (click to reveal)

3. **Get a phone number**:
   - In Twilio Console, go to "Phone Numbers"
   - Click "Get a number"
   - Choose a number (free with trial)
   - Copy the number (format: +1234567890)

### Step 3: Update .env File
```env
# Add these lines to backend/.env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### Step 4: Update Database
```bash
cd backend
python add_sms_fields.py
```

### Step 5: Add Your Phone Number
1. Login to your app
2. Go to **Settings**
3. Add your phone number (format: +919876543210 for India)
4. Enable "SMS Alerts"
5. Save

### Step 6: Test It!
```bash
cd backend
python test_sms.py
```

## 📱 Supported Countries

Twilio supports SMS in 200+ countries including:
- 🇮🇳 India: +91
- 🇺🇸 USA: +1
- 🇬🇧 UK: +44
- 🇦🇺 Australia: +61
- 🇨🇦 Canada: +1

## 💰 Pricing

**Free Trial**:
- $15 credit
- ~500 SMS messages
- Perfect for testing

**After Trial**:
- ~$0.0075 per SMS (India)
- ~$0.0079 per SMS (USA)
- Very affordable!

## 📧 Email vs SMS

| Feature | Email | SMS |
|---------|-------|-----|
| Setup | Gmail app password | Twilio account |
| Cost | Free | ~$0.01 per message |
| Delivery | Instant | Instant |
| Spam Risk | Medium | Low |
| Character Limit | Unlimited | 1600 chars |

**Recommendation**: Use both! Email for detailed reports, SMS for urgent alerts.

## 🧪 Testing

### Test SMS Service
```bash
cd backend
python test_sms.py
```

### Test Full Alert System
```bash
# Via API
curl -X POST http://localhost:5000/api/recommendations/send-alerts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Via UI
1. Go to AI Insights page
2. Click "Send Email Alert" button
3. Check your phone!
```

## 📝 SMS Message Format

```
🚨 Financial Alert for John

1. 🚨 Critical: Low Savings Rate
   Savings rate: 8.5%. Spending $4,200 vs income $4,600...

2. 💰 Reduce Expenses
   Cut non-essential spending by 15-20%...

Check dashboard: http://localhost:5173
```

## ⚙️ Configuration Options

### In User Preferences:
- **phone_number**: Your mobile number with country code
- **sms_alerts_enabled**: Toggle SMS notifications on/off

### In .env:
- **TWILIO_ACCOUNT_SID**: Your Twilio account ID
- **TWILIO_AUTH_TOKEN**: Your Twilio auth token
- **TWILIO_PHONE_NUMBER**: Your Twilio phone number

## 🔧 Troubleshooting

### "SMS service not configured"
- Check .env has all 3 Twilio variables
- Restart backend server after updating .env

### "Phone number not set"
- Go to Settings → Add phone number
- Enable "SMS Alerts"
- Format: +[country code][number] (e.g., +919876543210)

### "SMS not received"
- Check Twilio console logs: https://console.twilio.com/logs
- Verify phone number format includes country code
- Check Twilio trial restrictions (some countries blocked)

### "Invalid phone number"
- Must start with + and country code
- India: +91xxxxxxxxxx (10 digits)
- USA: +1xxxxxxxxxx (10 digits)

## 🌟 Features

✅ Automatic SMS alerts for high-risk situations  
✅ Configurable per user  
✅ Works alongside email alerts  
✅ Short, actionable messages  
✅ Direct link to dashboard  
✅ Priority-based filtering  

## 📊 When You'll Receive SMS

- **Critical**: Savings rate < 10%
- **Warning**: Savings rate < 20%
- **Emergency Fund**: Low reserves
- **Budget Exceeded**: Category overspending

## 🔐 Security

- Phone numbers encrypted in database
- Twilio credentials in .env (not in code)
- SMS only sent for high-priority alerts
- User can disable anytime

## 🎯 Next Steps

1. **Install**: `pip install twilio`
2. **Sign up**: https://www.twilio.com/try-twilio
3. **Configure**: Update .env with credentials
4. **Migrate**: Run `python add_sms_fields.py`
5. **Test**: Run `python test_sms.py`
6. **Use**: Add phone in Settings, enable SMS alerts

---

**SMS alerts make your financial monitoring even more powerful!** 📱💰
