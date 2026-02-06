import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import type { RootState } from './store/store';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import Transactions from './pages/Transactions';
import Analytics from './pages/Analytics';
import AIInsights from './pages/AIInsights';
import Settings from './pages/Settings';
import RiskPrediction from './pages/RiskPrediction';
import BudgetControl from './pages/BudgetControl';

function App() {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/register"
          element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/transactions"
          element={isAuthenticated ? <Transactions /> : <Navigate to="/login" />}
        />
        <Route
          path="/analytics"
          element={isAuthenticated ? <Analytics /> : <Navigate to="/login" />}
        />
        <Route
          path="/ai-insights"
          element={isAuthenticated ? <AIInsights /> : <Navigate to="/login" />}
        />
        <Route
          path="/risk-predictions"
          element={isAuthenticated ? <RiskPrediction /> : <Navigate to="/login" />}
        />
        <Route
          path="/budget-control"
          element={isAuthenticated ? <BudgetControl /> : <Navigate to="/login" />}
        />
        <Route
          path="/settings"
          element={isAuthenticated ? <Settings /> : <Navigate to="/login" />}
        />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
