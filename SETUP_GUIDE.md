# Quick Setup Guide

## Step-by-Step Installation

### 1. Install PostgreSQL

**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Run installer and set password for `postgres` user
- Default port: 5432

**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE expense_analyzer;

# Verify
\l

# Exit
\q
```

### 3. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# The database tables will be created automatically on first run
```

### 4. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# This will take a few minutes
```

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
  ➜  Local:   http://localhost:5173/
```

### 6. Access the Application

Open your browser and go to: `http://localhost:5173`

### 7. Create Your Account

1. Click "Register here"
2. Fill in:
   - Full Name: Your Name
   - Email: your@email.com
   - Password: (min 8 characters)
3. Click "Register"

You'll be automatically logged in and redirected to the dashboard!

## Troubleshooting

### Database Connection Error

**Error:** `could not connect to server`

**Solution:**
1. Make sure PostgreSQL is running:
   ```bash
   # Windows (in Services)
   Services → PostgreSQL → Start
   
   # macOS
   brew services restart postgresql@14
   
   # Linux
   sudo systemctl status postgresql
   ```

2. Check DATABASE_URL in `backend/.env`:
   ```
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/expense_analyzer
   ```

### Port Already in Use

**Error:** `Port 5000 is already in use`

**Solution:**
Change the port in `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Make sure virtual environment is activated
# You should see (venv) in your terminal

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Then install again
pip install -r requirements.txt
```

### Frontend Build Errors

**Error:** `Cannot find module '@mui/material'`

**Solution:**
```bash
cd frontend

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json  # macOS/Linux
# or
Remove-Item -Recurse node_modules, package-lock.json  # Windows PowerShell

# Reinstall
npm install
```

## Testing the AI Features

### 1. Add Sample Transactions

Add these transactions to see the AI in action:

**Income:**
- Amount: $5000
- Type: Income
- Description: "Monthly salary"
- Date: Current month

**Expenses:**
- $50 - "Starbucks coffee" → Auto-categorized as Food & Dining
- $100 - "Uber rides" → Auto-categorized as Transportation
- $200 - "Amazon purchase" → Auto-categorized as Shopping
- $150 - "Electric bill" → Auto-categorized as Bills & Utilities
- $80 - "Movie tickets" → Auto-categorized as Entertainment

### 2. View Your Risk Score

After adding transactions, your dashboard will show:
- Financial summary (income, expenses, savings)
- **Risk Score** - calculated based on your financial health
- **Expense Predictions** - AI forecast for next 3 months
- **Recommendations** - Personalized tips to improve finances

### 3. Explore Categories

- Dashboard shows pie chart of spending by category
- All categories are pre-configured
- You can add custom categories in Settings

## Default Categories

### Expense Categories
- 🍔 Food & Dining
- 🚗 Transportation
- 🛒 Shopping
- 📄 Bills & Utilities
- 🏥 Healthcare
- 🎬 Entertainment
- 📚 Education
- 📦 Others

### Income Categories
- 💰 Salary
- 💼 Business
- 📈 Investments
- 💵 Other Income

## Next Steps

1. **Set Budgets**
   - Go to Settings
   - Set monthly budget for each category
   - Track spending vs budget

2. **Regular Updates**
   - Add transactions regularly
   - Check recommendations weekly
   - Monitor risk score monthly

3. **Optimize Finances**
   - Act on AI recommendations
   - Reduce high-spending categories
   - Build emergency fund

## Need Help?

Check the main [README.md](./README.md) for:
- Detailed API documentation
- Architecture overview
- ML model explanations
- Advanced features

Happy tracking! 💰📊
