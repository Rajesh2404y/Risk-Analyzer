# 📱 SMS Alerts - Quick Start

## ✅ What I've Implemented

SMS alerts are now fully integrated into your Risk Analyzer app! You can receive financial alerts via text message.

## 🚀 Setup in 5 Minutes

### 1. Install Twilio
```bash
cd backend
pip install twilio
```

### 2. Get FREE Twilio Account
👉 **Sign up**: https://www.twilio.com/try-twilio

You'll get:
- $15 free credit
- ~500 free SMS messages
- No credit card needed for trial

### 3. Get Your Credentials

After signing up:
1. Go to: https://console.twilio.com
2. Copy these 3 things:
   - **Account SID** (starts with AC...)
   - **Auth Token** (click eye icon to reveal)
   - **Phone Number** (get one free from "Phone Numbers" section)

### 4. Update .env File

Add to `backend\.env`:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### 5. Update Database
```bash
cd backend
python add_sms_fields.py
```

### 6. Test It!
```bash
python test_sms.py +919876543210
```
(Replace with your actual phone number)

## 📱 Phone Number Format

**India**: +919876543210  
**USA**: +11234567890  
**UK**: +441234567890  

Always include the + and country code!

## 🎯 How It Works

1. **Add your phone** in Settings page
2. **Enable SMS alerts**
3. **Get instant notifications** when:
   - Savings rate drops below 10% (Critical)
   - Savings rate below 20% (Warning)
   - Budget exceeded
   - Emergency fund low

## 💡 Example SMS

```
🚨 Financial Alert for John

1. 🚨 Critical: Low Savings Rate
   Savings rate: 8.5%. Spending $4,200...

2. 💰 Reduce Expenses
   Cut non-essential spending by 15-20%...

Dashboard: http://localhost:5173
```

## 🆚 Email vs SMS

**Use Email for**:
- Detailed reports
- Multiple recommendations
- Charts and graphs

**Use SMS for**:
- Urgent alerts
- Quick notifications
- On-the-go updates

**Best**: Enable both!

## 💰 Cost

- **Trial**: FREE ($15 credit = ~500 messages)
- **After trial**: ~₹0.60 per SMS (India) or $0.01 (USA)
- Very affordable for occasional alerts

## ⚙️ Configuration

### In App Settings:
- Add phone number: +919876543210
- Toggle "SMS Alerts": ON

### In .env:
```env
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

## 🔧 Troubleshooting

### SMS not received?
1. Check Twilio logs: https://console.twilio.com/logs
2. Verify phone format: +[country][number]
3. Check trial restrictions (some countries blocked)

### "SMS service not configured"?
1. Check all 3 variables in .env
2. Restart backend: `python app.py`

### "Invalid phone number"?
- Must start with +
- Include country code
- Example: +919876543210 (not 9876543210)

## 📊 Features

✅ Instant SMS alerts  
✅ Works with email alerts  
✅ User-configurable  
✅ Priority-based (only urgent alerts)  
✅ Short, actionable messages  
✅ Direct dashboard link  

## 🎬 Next Steps

1. **Now**: `pip install twilio`
2. **Sign up**: https://www.twilio.com/try-twilio (2 min)
3. **Configure**: Add credentials to .env
4. **Migrate**: `python add_sms_fields.py`
5. **Test**: `python test_sms.py +your_number`
6. **Use**: Enable in Settings!

---

**Get instant financial alerts on your phone!** 📱💰

See `SMS_SETUP_GUIDE.md` for detailed documentation.
