# 🧪 Test All Dashboards with Sample Data

## Quick Start

### 1. Add Sample Transactions
```bash
cd backend
python add_sample_data.py YOUR_EMAIL
```

Example:
```bash
python add_sample_data.py user@example.com
```

This will add:
- ✅ 3 months of income ($5,000/month)
- ✅ 3 months of expenses (~$1,800/month)
- ✅ Multiple categories (Food, Transport, Bills, Shopping)
- ✅ Realistic transaction patterns

### 2. View All Dashboards

After adding data, visit:

1. **Dashboard** - http://localhost:5173/dashboard
   - Total income, expenses, savings
   - Monthly trends chart
   - Category breakdown
   - Recent transactions

2. **Transactions** - http://localhost:5173/transactions
   - List of all transactions
   - Filter by type, category, date
   - Add/Edit/Delete transactions

3. **Analytics** - http://localhost:5173/analytics
   - Spending trends over time
   - Category-wise breakdown
   - Monthly comparison
   - Visual charts

4. **Risk & Predictions** - http://localhost:5173/risk-predictions
   - Risk score calculation
   - Risk factors analysis
   - 6-month expense forecast
   - AI-powered predictions

5. **Budget Control** - http://localhost:5173/budget-control
   - Set category budgets
   - Track spending vs budget
   - Budget alerts

6. **AI Insights** - http://localhost:5173/ai-insights
   - AI-powered recommendations
   - Financial insights
   - Action items

7. **Settings** - http://localhost:5173/settings
   - Change password
   - Update preferences
   - Email notifications

## What You'll See

### Dashboard
- **Total Income**: $15,000
- **Total Expenses**: ~$5,500
- **Savings**: ~$9,500
- **Savings Rate**: ~63%
- **Charts**: Monthly trends, category breakdown

### Risk Score
- **Score**: ~20-30 (Low Risk)
- **Level**: Low
- **Factors**: All calculated from real data

### Predictions
- **Next 6 months**: Expense forecasts
- **Based on**: Your transaction history
- **Trend**: Slight increase expected

### Analytics
- **Spending Trends**: Line chart showing monthly expenses
- **Category Breakdown**: Pie chart of spending by category
- **Top Categories**: Bills (Rent), Food, Transport

## Sample Data Details

### Income (Monthly)
- Salary: $5,000

### Expenses (Monthly Average)
- Rent: $1,200
- Utilities: $150-170
- Food: $250-300
- Transport: $80-100
- Shopping: $120-200

### Total: ~$1,800-2,000/month

## Clean Up (Optional)

To remove sample data and start fresh:
```sql
-- In MySQL
DELETE FROM transactions WHERE user_id = YOUR_USER_ID;
```

Or just delete and recreate your account.

## Verify Everything Works

After adding sample data, check:

- [ ] Dashboard shows real numbers (not $0.00)
- [ ] Charts display data
- [ ] Risk score calculated (not 0)
- [ ] Predictions show future months
- [ ] Analytics charts render
- [ ] Transactions list populated
- [ ] No console errors
- [ ] All pages load correctly

## Troubleshooting

### "User not found"
- Register first at http://localhost:5173/register
- Then run the script with your registered email

### "No data showing"
- Refresh the page
- Check browser console for errors
- Verify backend is running (port 5000)

### "Risk score is 0"
- Wait a moment and refresh
- Risk calculation needs a few seconds

---

**Now your dashboards will show real, meaningful data!** 📊✨
