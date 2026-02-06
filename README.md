<<<<<<< HEAD
# Risk-Analyzer
=======
# AI-Based Personal Expense Risk Analyzer

A sophisticated full-stack application that leverages machine learning to help users track expenses, analyze spending behavior, predict future expenses, and assess financial risks with personalized AI-powered recommendations.

## 🚀 Features

### Core Features
- ✅ **Expense & Income Tracking** - Record and categorize all financial transactions
- ✅ **AI-Powered Auto-Categorization** - Automatically categorize expenses using ML
- ✅ **Risk Score Calculation** - Comprehensive financial health assessment (0-100 scale)
- ✅ **Expense Prediction** - Time series forecasting for future expenses
- ✅ **Personalized Recommendations** - AI-generated insights and action items
- ✅ **Interactive Dashboard** - Real-time visualization of financial data
- ✅ **Budget Management** - Set and track budgets by category
- ✅ **Analytics & Insights** - Deep dive into spending patterns

### AI/ML Capabilities
- **Expense Categorization** using Naive Bayes classifier with TF-IDF features
- **Risk Assessment** based on multiple financial health factors
- **Expense Forecasting** using time series analysis and linear regression
- **Smart Recommendations** using rule-based and ML hybrid approach

## 🏗️ Architecture

### Tech Stack

#### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI) v7
- **CSS**: Tailwind CSS v4
- **State Management**: Redux Toolkit
- **API Client**: Axios
- **Charts**: MUI X-Charts
- **Routing**: React Router v7

#### Backend
- **Framework**: Flask (Python 3.12)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (Flask-JWT-Extended)
- **ML Libraries**: 
  - Pandas & NumPy (data manipulation)
  - Scikit-learn (classification)
  - Prophet/Linear Regression (forecasting)
  - NLTK (text processing)

## 📋 Prerequisites

- **Node.js** v20.19+ or v22.12+
- **Python** 3.12+
- **PostgreSQL** 12+
- **npm** or **yarn** or **pnpm**
- **pip** (Python package manager)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Risk-Analyzer
```

### 2. Database Setup

Create a PostgreSQL database:
```sql
CREATE DATABASE expense_analyzer;
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and configure:
# - SECRET_KEY
# - JWT_SECRET_KEY
# - DATABASE_URL=postgresql://username:password@localhost:5432/expense_analyzer
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 5. Start Backend Server

```bash
# In backend directory
python app.py
```

The backend API will be available at `http://localhost:5000`

## 🎯 Usage

### First Time Setup

1. **Register an Account**
   - Navigate to `http://localhost:5173/register`
   - Create your account with email and password

2. **Login**
   - Use your credentials to login

3. **Add Transactions**
   - Navigate to Transactions page
   - Add income and expense transactions
   - The AI will automatically categorize your expenses!

4. **View Dashboard**
   - See your financial summary
   - Check your Risk Score (0-100)
   - Review AI-powered predictions
   - Act on personalized recommendations

### Key Workflows

#### Adding Transactions
1. Go to Transactions
2. Click "Add Transaction"
3. Enter details (amount, description, merchant)
4. AI auto-categorizes or select manually
5. Save

#### Understanding Risk Score
The risk score (0-100) is calculated based on:
- **Spending Velocity** (25%) - Rate of spending increase
- **Savings Rate** (20%) - Income vs expenses ratio
- **Budget Adherence** (10%) - How well you stick to budgets
- **Category Concentration** (10%) - Spending distribution
- **Emergency Fund** (15%) - Months of coverage
- **Debt-to-Income** (20%) - Debt burden

**Risk Levels:**
- **0-30**: Low Risk (Healthy finances)
- **31-60**: Medium Risk (Needs attention)
- **61-100**: High Risk (Take immediate action)

#### Setting Budgets
1. Go to Settings
2. Set monthly budgets by category
3. Track actual vs budgeted spending
4. Get alerts when approaching limits

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Transactions
- `GET /api/transactions` - List transactions
- `POST /api/transactions` - Create transaction
- `PUT /api/transactions/:id` - Update transaction
- `DELETE /api/transactions/:id` - Delete transaction

### Analytics
- `GET /api/analytics/summary` - Financial summary
- `GET /api/analytics/trends` - Spending trends
- `GET /api/analytics/category-breakdown` - Category analysis

### AI/ML Features
- `GET /api/risk/score` - Calculate current risk score
- `GET /api/predictions/expenses` - Predict future expenses
- `GET /api/recommendations` - Get AI recommendations

### Categories & Budgets
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create custom category
- `GET /api/budgets` - List budgets
- `POST /api/budgets` - Create budget

## 🤖 AI/ML Models

### 1. Expense Categorization Model
- **Algorithm**: Naive Bayes with TF-IDF vectorization
- **Features**: Transaction description, merchant name
- **Categories**: Food & Dining, Transportation, Shopping, Bills, Healthcare, Entertainment, Education, Others
- **Accuracy**: Improves with usage as model learns from corrections

### 2. Risk Scoring System
- **Type**: Weighted scoring algorithm
- **Factors**: 6 key financial health indicators
- **Output**: Score (0-100) and risk level (low/medium/high)
- **Real-time**: Recalculated after each transaction

### 3. Expense Prediction Model
- **Algorithm**: Linear regression on time series data
- **Input**: Historical expenses (6 months minimum)
- **Output**: Monthly predictions for next 3 months with confidence intervals
- **Granularity**: Weekly aggregation for smoother predictions

### 4. Recommendation Engine
- **Type**: Hybrid (rule-based + collaborative filtering)
- **Inputs**: Risk factors, spending patterns, budgets
- **Output**: Prioritized list of actionable recommendations
- **Categories**: Budget alerts, savings opportunities, risk mitigation, behavioral insights

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- SQL injection prevention via SQLAlchemy ORM
- CORS configuration
- Input validation on all endpoints
- Secure token storage

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📈 Future Enhancements

- [ ] Bank account integration (Plaid API)
- [ ] Receipt scanning with OCR
- [ ] Voice input for transactions
- [ ] Multi-currency support
- [ ] Family/shared accounts
- [ ] Mobile app (React Native)
- [ ] Deep learning models for better predictions
- [ ] Anomaly detection for unusual spending
- [ ] Goal-based financial planning
- [ ] Export reports (PDF, Excel)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

Senior AI Software Architect

## 🙏 Acknowledgments

- MUI for the excellent component library
- Scikit-learn for ML capabilities
- Flask for the robust backend framework
- The open-source community

---

**Built with ❤️ using React, Flask, and Machine Learning**

For detailed architecture and design decisions, see [ARCHITECTURE.md](./ARCHITECTURE.md)
>>>>>>> 7e5fb9b (Initial commit)
