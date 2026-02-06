# Email Configuration Setup Guide

## Quick Fix for Email Error

The "Failed to send email" error occurs because the email service is not properly configured. Follow these steps to fix it:

### Step 1: Configure Gmail App Password (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to [Google Account Settings](https://myaccount.google.com/apppasswords)
   - Select "Mail" and your device
   - Copy the 16-character password generated

### Step 2: Update .env File

Edit your `backend/.env` file and replace the placeholder values:

```env
# Replace these placeholder values with real credentials:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-actual-email@gmail.com
SMTP_PASSWORD=your-16-character-app-password
FROM_EMAIL=your-actual-email@gmail.com
FROM_NAME=Expense Risk Analyzer
```

### Step 3: Restart Backend Server

```bash
cd backend
python app.py
```

### Alternative Email Providers

#### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

#### Yahoo Mail
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

### Testing Email Configuration

1. Open the dashboard at `http://localhost:5173/dashboard`
2. Click "Send Alert Email" button
3. Check for success message

### Troubleshooting

- **"Authentication failed"**: Check username/password
- **"Connection refused"**: Check SMTP host/port
- **"Service not configured"**: Ensure .env values are not placeholders
- **Still not working?**: Check spam folder or try different email provider

### Security Notes

- Never commit real credentials to version control
- Use App Passwords instead of regular passwords
- Keep your .env file in .gitignore