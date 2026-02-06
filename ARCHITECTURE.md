# AI-Based Personal Expense Risk Analyzer - System Architecture

## 📋 Executive Summary

The AI-Based Personal Expense Risk Analyzer is a sophisticated financial management system that leverages machine learning to help users track expenses, analyze spending behavior, predict future expenses, and assess financial risks. The system provides actionable insights and personalized recommendations to improve financial health.

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │   React Frontend (Vite + TypeScript + MUI v7)          │ │
│  │   - Dashboard │ Analytics │ Transactions │ Settings    │ │
│  │   - Redux Toolkit (State) │ Chart.js (Viz)            │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │          Flask Backend (Python 3.12)                   │ │
│  │                                                        │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │ │
│  │  │ REST API     │  │ Business     │  │ Auth        │ │ │
│  │  │ Endpoints    │  │ Logic        │  │ Middleware  │ │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    AI/ML Layer                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │    Machine Learning Pipeline                           │ │
│  │                                                        │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │ │
│  │  │ Expense      │  │ Risk Score   │  │ Time Series │ │ │
│  │  │ Categorizer  │  │ Calculator   │  │ Predictor   │ │ │
│  │  │ (Scikit)     │  │ (Custom)     │  │ (Prophet)   │ │ │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │ │
│  │                                                        │ │
│  │  ┌──────────────┐  ┌──────────────┐                  │ │
│  │  │ Feature      │  │ Recommender  │                  │ │
│  │  │ Engineering  │  │ System       │                  │ │
│  │  └──────────────┘  └──────────────┘                  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │   PostgreSQL Database (SQLAlchemy ORM)                 │ │
│  │                                                        │ │
│  │   Tables: users │ transactions │ categories │ budgets │ │
│  │          risk_scores │ predictions │ user_preferences  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Module Breakdown

### Frontend Modules

#### 1. **Dashboard Module**
- **Purpose**: Main overview of financial health
- **Components**:
  - `DashboardLayout`: Main container
  - `FinancialSummaryCard`: Total income, expenses, savings
  - `RiskScoreCard`: Visual risk indicator
  - `ExpenseTrendChart`: Line chart for spending trends
  - `CategoryBreakdownChart`: Pie chart for expense categories
  - `RecentTransactions`: Latest transactions list
  - `RecommendationsPanel`: AI-generated suggestions

#### 2. **Transaction Management Module**
- **Purpose**: Record and manage income/expenses
- **Components**:
  - `TransactionList`: Data grid with filters
  - `AddTransactionForm`: Form with auto-categorization
  - `TransactionDetails`: Detailed view/edit
  - `BulkImport`: CSV/Excel upload functionality

#### 3. **Analytics Module**
- **Purpose**: Deep dive into spending patterns
- **Components**:
  - `SpendingAnalytics`: Time-based analysis
  - `CategoryComparison`: Month-over-month comparison
  - `PredictionChart`: Future expense predictions
  - `BudgetTracker`: Budget vs actual spending

#### 4. **Settings Module**
- **Purpose**: User preferences and configuration
- **Components**:
  - `ProfileSettings`: User information
  - `BudgetSettings`: Set category budgets
  - `NotificationSettings`: Alert preferences
  - `CategoryManagement`: Custom categories

### Backend Modules

#### 1. **API Module** (`/backend/api`)
```
api/
├── routes/
│   ├── auth.py           # Authentication endpoints
│   ├── transactions.py   # CRUD for transactions
│   ├── analytics.py      # Analytics endpoints
│   ├── predictions.py    # ML predictions
│   └── recommendations.py # AI recommendations
└── middleware/
    ├── auth_middleware.py
    └── error_handler.py
```

#### 2. **ML Module** (`/backend/ml`)
```
ml/
├── categorizer.py        # Expense categorization
├── risk_calculator.py    # Risk scoring algorithm
├── predictor.py          # Time series forecasting
├── feature_engineering.py # Feature extraction
├── recommender.py        # Recommendation engine
└── models/               # Trained model files
    ├── category_model.pkl
    └── prediction_model.pkl
```

#### 3. **Database Module** (`/backend/database`)
```
database/
├── models.py             # SQLAlchemy models
├── schemas.py            # Pydantic schemas
└── migrations/           # Database migrations
```

---

## 🔄 Data Flow

### 1. Transaction Creation Flow
```
User Input → Frontend Form
    ↓
Validation (Redux)
    ↓
POST /api/transactions
    ↓
Flask API Endpoint
    ↓
ML Categorization (auto-categorize)
    ↓
Save to Database
    ↓
Trigger Risk Recalculation
    ↓
Return Updated Data
    ↓
Update Frontend State
```

### 2. Risk Assessment Flow
```
New Transaction Added
    ↓
Fetch User Financial History
    ↓
Calculate Features:
  - Spending velocity
  - Category concentration
  - Income stability
  - Debt-to-income ratio
  - Emergency fund coverage
    ↓
Risk Scoring Algorithm:
  - Low Risk (0-30)
  - Medium Risk (31-60)
  - High Risk (61-100)
    ↓
Store Risk Score
    ↓
Generate Recommendations
```

### 3. Prediction Flow
```
User Requests Prediction
    ↓
Fetch Historical Data (6-12 months)
    ↓
Feature Engineering:
  - Seasonal patterns
  - Day-of-week trends
  - Category trends
    ↓
Time Series Model (Prophet/ARIMA)
    ↓
Generate Predictions (1-3 months ahead)
    ↓
Confidence Intervals
    ↓
Return to Frontend
```

---

## 🤖 AI/ML Logic

### 1. **Expense Categorization**

**Algorithm**: Naive Bayes / Random Forest Classifier

**Features**:
- Transaction description (TF-IDF)
- Amount range
- Merchant name
- Time of day/week
- Historical patterns

**Categories**:
- Food & Dining
- Transportation
- Shopping
- Bills & Utilities
- Healthcare
- Entertainment
- Education
- Others

**Implementation**:
```python
# Pseudo-code
def categorize_expense(transaction):
    features = extract_features(transaction)
    category = trained_model.predict(features)
    confidence = trained_model.predict_proba(features)
    return category, confidence
```

### 2. **Risk Score Calculation**

**Methodology**: Weighted Scoring System

**Risk Factors** (Total = 100 points):

| Factor | Weight | Calculation |
|--------|--------|-------------|
| Spending Velocity | 25% | (Monthly Expenses - Avg) / Avg |
| Debt-to-Income | 20% | Total Debt / Monthly Income |
| Savings Rate | 20% | Savings / Income |
| Emergency Fund | 15% | Months of expenses covered |
| Budget Adherence | 10% | Actual vs Budget variance |
| Category Concentration | 10% | Single category dominance |

**Risk Levels**:
- **Low (0-30)**: Healthy financial habits
- **Medium (31-60)**: Needs attention
- **High (61-100)**: Critical issues

**Implementation**:
```python
def calculate_risk_score(user_data):
    score = 0
    
    # Spending velocity (0-25)
    velocity = calculate_spending_velocity(user_data)
    score += min(velocity * 5, 25)
    
    # Debt-to-income (0-20)
    dti_ratio = user_data.debt / user_data.income
    score += min(dti_ratio * 40, 20)
    
    # Savings rate (0-20, inverse)
    savings_rate = user_data.savings / user_data.income
    score += max(20 - savings_rate * 100, 0)
    
    # Emergency fund (0-15, inverse)
    months_covered = user_data.emergency_fund / user_data.monthly_expenses
    score += max(15 - months_covered * 3, 0)
    
    # Budget adherence (0-10)
    variance = calculate_budget_variance(user_data)
    score += min(variance * 10, 10)
    
    # Category concentration (0-10)
    concentration = calculate_category_concentration(user_data)
    score += min(concentration * 10, 10)
    
    return min(score, 100)
```

### 3. **Expense Prediction**

**Algorithm**: Facebook Prophet / ARIMA

**Features**:
- Historical spending data
- Seasonal components (yearly, monthly, weekly)
- Holidays and special events
- Trend components
- Category-wise patterns

**Process**:
1. **Data Preparation**: Aggregate daily/weekly expenses
2. **Trend Analysis**: Identify upward/downward trends
3. **Seasonality Detection**: Weekly, monthly patterns
4. **Model Training**: Fit Prophet model
5. **Forecasting**: Predict next 1-3 months
6. **Confidence Intervals**: 80% and 95% intervals

**Implementation**:
```python
from prophet import Prophet

def predict_expenses(user_id, months_ahead=3):
    # Fetch historical data
    data = get_user_transactions(user_id)
    df = prepare_prophet_data(data)
    
    # Train model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    model.fit(df)
    
    # Make predictions
    future = model.make_future_dataframe(periods=months_ahead*30)
    forecast = model.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
```

### 4. **Recommendation Engine**

**Rule-Based + ML Hybrid Approach**

**Recommendation Types**:

1. **Budget Recommendations**
   - Based on income and historical spending
   - 50/30/20 rule: 50% needs, 30% wants, 20% savings

2. **Savings Opportunities**
   - Identify high-spending categories
   - Compare with similar users (collaborative filtering)

3. **Risk Mitigation**
   - Specific actions based on risk factors
   - Emergency fund building
   - Debt reduction strategies

4. **Behavioral Insights**
   - Spending pattern anomalies
   - Recurring subscriptions
   - Unusual transactions

**Implementation**:
```python
def generate_recommendations(user_id):
    user = get_user_data(user_id)
    risk_score = calculate_risk_score(user)
    recommendations = []
    
    # High spending categories
    top_categories = get_top_spending_categories(user)
    for cat in top_categories[:3]:
        if cat.percentage > 30:
            recommendations.append({
                'type': 'budget_alert',
                'category': cat.name,
                'message': f'Reduce {cat.name} spending by 15%',
                'potential_savings': cat.amount * 0.15
            })
    
    # Emergency fund
    if user.emergency_fund < user.monthly_expenses * 3:
        recommendations.append({
            'type': 'savings',
            'message': 'Build emergency fund to 3 months',
            'action': 'Save $X per month'
        })
    
    # Debt reduction
    if user.debt_to_income > 0.4:
        recommendations.append({
            'type': 'debt',
            'message': 'High debt-to-income ratio',
            'action': 'Focus on debt payoff'
        })
    
    return recommendations
```

---

## 🗄️ Database Schema

### Tables

#### 1. **users**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. **transactions**
```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    type VARCHAR(20) NOT NULL, -- 'income' or 'expense'
    amount DECIMAL(10, 2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    description TEXT,
    transaction_date DATE NOT NULL,
    merchant VARCHAR(255),
    payment_method VARCHAR(50),
    is_recurring BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. **categories**
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id), -- NULL for system categories
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL, -- 'income' or 'expense'
    icon VARCHAR(50),
    color VARCHAR(20),
    is_system BOOLEAN DEFAULT FALSE
);
```

#### 4. **budgets**
```sql
CREATE TABLE budgets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    category_id INTEGER REFERENCES categories(id),
    amount DECIMAL(10, 2) NOT NULL,
    period VARCHAR(20) DEFAULT 'monthly', -- 'weekly', 'monthly', 'yearly'
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. **risk_scores**
```sql
CREATE TABLE risk_scores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    score INTEGER NOT NULL, -- 0-100
    risk_level VARCHAR(20), -- 'low', 'medium', 'high'
    factors JSONB, -- Detailed breakdown
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 6. **predictions**
```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    prediction_date DATE NOT NULL,
    predicted_amount DECIMAL(10, 2),
    confidence_lower DECIMAL(10, 2),
    confidence_upper DECIMAL(10, 2),
    category_id INTEGER REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 7. **user_preferences**
```sql
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) UNIQUE,
    currency VARCHAR(10) DEFAULT 'USD',
    notification_enabled BOOLEAN DEFAULT TRUE,
    risk_alert_threshold INTEGER DEFAULT 60,
    theme VARCHAR(20) DEFAULT 'light',
    preferences JSONB, -- Additional settings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

### Transactions
- `GET /api/transactions` - List all transactions (with filters)
- `POST /api/transactions` - Create transaction
- `GET /api/transactions/:id` - Get transaction details
- `PUT /api/transactions/:id` - Update transaction
- `DELETE /api/transactions/:id` - Delete transaction
- `POST /api/transactions/bulk` - Bulk import transactions

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create custom category
- `PUT /api/categories/:id` - Update category
- `DELETE /api/categories/:id` - Delete category

### Analytics
- `GET /api/analytics/summary` - Financial summary
- `GET /api/analytics/trends` - Spending trends
- `GET /api/analytics/category-breakdown` - Category analysis
- `GET /api/analytics/comparison` - Period comparison

### Risk & Predictions
- `GET /api/risk/score` - Current risk score
- `GET /api/risk/history` - Risk score history
- `GET /api/predictions/expenses` - Predicted expenses
- `GET /api/recommendations` - Personalized recommendations

### Budgets
- `GET /api/budgets` - List budgets
- `POST /api/budgets` - Create budget
- `PUT /api/budgets/:id` - Update budget
- `DELETE /api/budgets/:id` - Delete budget

---

## 🎨 Frontend Technology Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI) v7
- **CSS**: Tailwind CSS v4
- **State Management**: Redux Toolkit
- **API Client**: Axios
- **Charts**: MUI X-Charts
- **Routing**: React Router v7
- **Form Handling**: React Hook Form
- **Validation**: Zod
- **Date Handling**: date-fns
- **Icons**: Material Design Icons

---

## 🐍 Backend Technology Stack

- **Framework**: Flask
- **Runtime**: Python 3.12
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migration**: Alembic
- **API Documentation**: Flask-RESTX / Swagger
- **Authentication**: Flask-JWT-Extended
- **Validation**: Marshmallow
- **Testing**: PyTest
- **ML Libraries**:
  - Pandas (data manipulation)
  - NumPy (numerical operations)
  - Scikit-learn (classification)
  - Prophet (time series forecasting)
  - NLTK (text processing)

---

## 🚀 Deployment Architecture

### Development
- Frontend: `localhost:5173` (Vite dev server)
- Backend: `localhost:5000` (Flask dev server)
- Database: Local PostgreSQL

### Production
- Frontend: Static hosting (Vercel/Netlify)
- Backend: Cloud platform (AWS/GCP/Azure)
- Database: Managed PostgreSQL (RDS/Cloud SQL)
- Cache: Redis (optional)
- File Storage: S3 (for bulk imports)

---

## 🔒 Security Considerations

1. **Authentication**:
   - JWT-based authentication
   - Secure password hashing (bcrypt)
   - Token refresh mechanism

2. **Data Protection**:
   - SQL injection prevention (ORM)
   - XSS protection
   - CSRF tokens
   - HTTPS only

3. **Privacy**:
   - User data encryption
   - GDPR compliance
   - Data anonymization for ML training

4. **API Security**:
   - Rate limiting
   - Input validation
   - CORS configuration

---

## 📊 Performance Optimization

1. **Frontend**:
   - Code splitting
   - Lazy loading
   - Memoization
   - Virtual scrolling for large lists

2. **Backend**:
   - Database indexing
   - Query optimization
   - Caching (Redis)
   - Batch processing for ML

3. **ML**:
   - Model caching
   - Asynchronous predictions
   - Pre-computed features

---

## 🧪 Testing Strategy

1. **Frontend**:
   - Unit tests (Vitest)
   - Component tests (React Testing Library)
   - E2E tests (Playwright)

2. **Backend**:
   - Unit tests (PyTest)
   - Integration tests
   - API tests

3. **ML**:
   - Model accuracy tests
   - Cross-validation
   - A/B testing for recommendations

---

## 📈 Future Enhancements

1. **Advanced Features**:
   - Bank account integration (Plaid API)
   - Receipt scanning (OCR)
   - Voice input for transactions
   - Multi-currency support

2. **AI Improvements**:
   - Deep learning models
   - Anomaly detection
   - Goal-based planning
   - Personalized insights

3. **Collaboration**:
   - Family accounts
   - Shared budgets
   - Financial advisor integration

---

## 📝 Conclusion

This architecture provides a robust foundation for an AI-powered personal finance application. The modular design allows for easy maintenance and scalability, while the ML components deliver intelligent insights to help users make better financial decisions.
