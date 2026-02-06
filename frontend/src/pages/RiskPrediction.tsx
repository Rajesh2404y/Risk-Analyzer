import { useEffect, useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Card,
  CardContent,
  Stack,
  Chip,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Warning,
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Error as ErrorIcon,
  Speed,
  Savings,
  AccountBalanceWallet,
  PieChart as PieChartIcon,
} from '@mui/icons-material';
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
import { LineChart } from '@mui/x-charts/LineChart';
import { riskAPI, predictionsAPI } from '../services/api';
import DashboardLayout from '../components/DashboardLayout';

interface RiskFactor {
  score: number;
  trend?: number;
  average_monthly?: number;
  last_month?: number;
  rate?: number;
  note?: string;
  over_budget?: number;
  total_budgets?: number;
  concentration?: number;
  top_category?: string;
  top_percentage?: number;
  months_covered?: number;
  ratio?: number;
  error?: string;
}

interface RiskData {
  score: number;
  risk_level: string;
  factors: {
    spending_velocity: RiskFactor;
    savings_rate: RiskFactor;
    budget_adherence: RiskFactor;
    category_concentration: RiskFactor;
    emergency_fund: RiskFactor;
    debt_to_income: RiskFactor;
  };
}

interface Prediction {
  date: string;
  predicted_amount: number;
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
};

const getRiskColor = (level: string): 'success' | 'warning' | 'error' => {
  switch (level) {
    case 'low': return 'success';
    case 'medium': return 'warning';
    case 'high': return 'error';
    default: return 'warning';
  }
};

const getGaugeColor = (score: number): string => {
  if (score < 35) return '#4caf50';
  if (score < 65) return '#ff9800';
  return '#f44336';
};

const getFactorIcon = (factorName: string) => {
  switch (factorName) {
    case 'spending_velocity': return <Speed />;
    case 'savings_rate': return <Savings />;
    case 'budget_adherence': return <AccountBalanceWallet />;
    case 'category_concentration': return <PieChartIcon />;
    case 'emergency_fund': return <CheckCircle />;
    case 'debt_to_income': return <ErrorIcon />;
    default: return <Warning />;
  }
};

const formatFactorName = (name: string): string => {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const getFactorDescription = (name: string, factor: RiskFactor): string => {
  switch (name) {
    case 'spending_velocity':
      if (factor.trend !== undefined) {
        const trend = Number(factor.trend);
        return `Your spending has ${trend > 0 ? 'increased' : 'decreased'} by ${Math.abs(trend).toFixed(1)}% over the last 3 months. Average monthly spending: ${formatCurrency(Number(factor.average_monthly) || 0)}.`;
      }
      return 'Insufficient data to calculate spending trend.';
    case 'savings_rate':
      if (factor.rate !== undefined) {
        const rate = Number(factor.rate);
        return `Your current savings rate is ${rate.toFixed(1)}%. ${rate >= 20 ? 'Great job!' : rate >= 10 ? 'Consider increasing savings.' : 'Critical: Increase your savings rate.'}`;
      }
      return factor.note || 'No income data available.';
    case 'budget_adherence':
      if (factor.over_budget !== undefined && factor.total_budgets !== undefined) {
        return `${factor.over_budget} out of ${factor.total_budgets} budgets are over limit. ${factor.over_budget === 0 ? 'Excellent budget management!' : 'Review your spending in over-budget categories.'}`;
      }
      return 'No budgets set up yet.';
    case 'category_concentration':
      if (factor.top_category && factor.top_percentage !== undefined) {
        const percentage = Number(factor.top_percentage);
        return `${percentage.toFixed(1)}% of spending is in "${factor.top_category}". ${percentage > 50 ? 'Consider diversifying your spending.' : 'Good spending distribution.'}`;
      }
      return 'Spending is well distributed across categories.';
    case 'emergency_fund':
      return factor.note || 'Emergency fund tracking not implemented yet.';
    case 'debt_to_income':
      return factor.note || 'Debt tracking not implemented yet.';
    default:
      return 'No additional information available.';
  }
};

const getFactorImpact = (score: number): { level: 'low' | 'medium' | 'high'; color: string } => {
  if (score <= 7) return { level: 'low', color: '#4caf50' };
  if (score <= 15) return { level: 'medium', color: '#ff9800' };
  return { level: 'high', color: '#f44336' };
};

function RiskPrediction() {
  const [loading, setLoading] = useState(true);
  const [riskData, setRiskData] = useState<RiskData | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [riskRes, predictionsRes] = await Promise.all([
        riskAPI.getRiskScore(),
        predictionsAPI.getPredictions(6),
      ]);

      setRiskData(riskRes.data);
      setPredictions(predictionsRes.data.predictions || []);
    } catch (err) {
      console.error('Error loading risk data:', err);
      setError('Failed to load risk data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getRiskExplanation = (score: number, level: string): string => {
    if (level === 'low') {
      return `Your financial risk score of ${score}/100 indicates excellent financial health. Your spending patterns are stable, savings rate is healthy, and you're adhering well to your budgets.`;
    } else if (level === 'medium') {
      return `Your financial risk score of ${score}/100 indicates moderate financial risk. There are some areas that need attention. Review the risk factors below to understand what's impacting your score.`;
    } else {
      return `Your financial risk score of ${score}/100 indicates high financial risk. Immediate action is recommended. Focus on the high-impact risk factors listed below to improve your financial health.`;
    }
  };

  if (loading) {
    return (
      <DashboardLayout title="Risk & Predictions">
        <Container maxWidth="xl" className="py-8">
          <Box className="flex justify-center items-center" sx={{ minHeight: '400px' }}>
            <CircularProgress />
          </Box>
        </Container>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Risk & Predictions">
      <Container maxWidth="xl" className="py-8">
        <Stack spacing={3}>
          {/* Header */}
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 600 }}>
              Risk & Prediction Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Comprehensive AI-powered analysis of your financial risk and future expense predictions
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" onClose={() => setError(null)}>
              {error}
            </Alert>
          )}

          {/* Risk Score Section */}
          <Stack direction={{ xs: 'column', lg: 'row' }} spacing={3}>
            {/* Gauge Card */}
            <Card sx={{ flex: 1, minHeight: 380 }}>
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="center" className="mb-4">
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Financial Risk Score
                  </Typography>
                  <Chip
                    label={riskData?.risk_level.toUpperCase() || 'N/A'}
                    color={getRiskColor(riskData?.risk_level || '')}
                    size="medium"
                    sx={{ fontWeight: 600 }}
                  />
                </Stack>

                <Box className="flex justify-center items-center" sx={{ height: 220 }}>
                  <Gauge
                    value={riskData?.score || 0}
                    valueMax={100}
                    startAngle={-110}
                    endAngle={110}
                    sx={{
                      width: 280,
                      height: 220,
                      [`& .${gaugeClasses.valueText}`]: {
                        fontSize: 40,
                        fontWeight: 700,
                      },
                      [`& .${gaugeClasses.valueArc}`]: {
                        fill: getGaugeColor(riskData?.score || 0),
                      },
                      [`& .${gaugeClasses.referenceArc}`]: {
                        fill: '#e0e0e0',
                      },
                    }}
                    text={({ value }) => `${value}`}
                  />
                </Box>

                <Stack direction="row" justifyContent="space-between" className="mt-2 px-4">
                  <Typography variant="caption" color="success.main" sx={{ fontWeight: 500 }}>
                    Low Risk (0-35)
                  </Typography>
                  <Typography variant="caption" color="warning.main" sx={{ fontWeight: 500 }}>
                    Medium (35-65)
                  </Typography>
                  <Typography variant="caption" color="error.main" sx={{ fontWeight: 500 }}>
                    High Risk (65-100)
                  </Typography>
                </Stack>
              </CardContent>
            </Card>

            {/* Risk Explanation Card */}
            <Card sx={{ flex: 1.5 }}>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  Risk Score Explanation
                </Typography>

                <Alert
                  severity={getRiskColor(riskData?.risk_level || '')}
                  icon={<Warning />}
                  sx={{ mb: 3 }}
                >
                  {getRiskExplanation(riskData?.score || 0, riskData?.risk_level || '')}
                </Alert>

                <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 2 }}>
                  Key Insights:
                </Typography>

                <Stack spacing={1}>
                  {riskData?.score !== undefined && riskData.score < 35 && (
                    <Stack direction="row" alignItems="center" spacing={1}>
                      <CheckCircle color="success" fontSize="small" />
                      <Typography variant="body2">Your finances are well-managed</Typography>
                    </Stack>
                  )}
                  {riskData?.factors?.spending_velocity?.trend !== undefined && (
                    <Stack direction="row" alignItems="center" spacing={1}>
                      {Number(riskData.factors.spending_velocity.trend) > 0 ? (
                        <TrendingUp color="error" fontSize="small" />
                      ) : (
                        <TrendingDown color="success" fontSize="small" />
                      )}
                      <Typography variant="body2">
                        Spending trend: {Number(riskData.factors.spending_velocity.trend) > 0 ? '+' : ''}
                        {Number(riskData.factors.spending_velocity.trend).toFixed(1)}%
                      </Typography>
                    </Stack>
                  )}
                  {riskData?.factors?.savings_rate?.rate !== undefined && (
                    <Stack direction="row" alignItems="center" spacing={1}>
                      <Savings color={Number(riskData.factors.savings_rate.rate) >= 20 ? 'success' : 'warning'} fontSize="small" />
                      <Typography variant="body2">
                        Savings rate: {Number(riskData.factors.savings_rate.rate).toFixed(1)}%
                      </Typography>
                    </Stack>
                  )}
                </Stack>
              </CardContent>
            </Card>
          </Stack>

          {/* Risk Factors Accordion */}
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Risk Factors Analysis
              </Typography>

              {riskData?.factors && Object.entries(riskData.factors).map(([name, factor]) => {
                const impact = getFactorImpact(factor.score);
                return (
                  <Accordion key={name} elevation={0} sx={{ border: '1px solid', borderColor: 'divider', mb: 1 }}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Stack direction="row" alignItems="center" spacing={2} sx={{ width: '100%', pr: 2 }}>
                        <Box sx={{ color: impact.color }}>
                          {getFactorIcon(name)}
                        </Box>
                        <Box sx={{ flex: 1 }}>
                          <Typography sx={{ fontWeight: 500 }}>
                            {formatFactorName(name)}
                          </Typography>
                        </Box>
                        <Chip
                          label={`${impact.level.toUpperCase()} IMPACT`}
                          size="small"
                          sx={{
                            backgroundColor: `${impact.color}20`,
                            color: impact.color,
                            fontWeight: 600,
                            fontSize: '0.7rem',
                          }}
                        />
                        <Box sx={{ width: 100, display: 'flex', alignItems: 'center', gap: 1 }}>
                          <LinearProgress
                            variant="determinate"
                            value={(factor.score / 25) * 100}
                            sx={{
                              flex: 1,
                              height: 6,
                              borderRadius: 3,
                              backgroundColor: '#e0e0e0',
                              '& .MuiLinearProgress-bar': {
                                backgroundColor: impact.color,
                                borderRadius: 3,
                              },
                            }}
                          />
                          <Typography variant="caption" sx={{ fontWeight: 600, minWidth: 20 }}>
                            {factor.score}
                          </Typography>
                        </Box>
                      </Stack>
                    </AccordionSummary>
                    <AccordionDetails sx={{ backgroundColor: 'grey.50' }}>
                      <Typography variant="body2" color="text.secondary">
                        {getFactorDescription(name, factor)}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                );
              })}
            </CardContent>
          </Card>

          {/* Expense Forecast */}
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                AI-Powered Expense Forecast (Next 6 Months)
              </Typography>

              {predictions.length > 0 ? (
                <>
                  <LineChart
                    xAxis={[
                      {
                        data: predictions.map((_, index) => index),
                        scaleType: 'point',
                        valueFormatter: (value) => {
                          const pred = predictions[value];
                          if (!pred?.date) return '';
                          const date = new Date(pred.date);
                          return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
                        },
                      },
                    ]}
                    series={[
                      {
                        data: predictions.map(p => p.predicted_amount),
                        label: 'Predicted Expenses',
                        area: true,
                        showMark: true,
                        color: '#1976d2',
                      },
                    ]}
                    height={350}
                  />

                  {/* Prediction Summary */}
                  <Stack direction={{ xs: 'column', md: 'row' }} spacing={3} className="mt-4">
                    {predictions.slice(0, 3).map((pred, index) => (
                      <Card key={index} variant="outlined" sx={{ flex: 1, backgroundColor: 'grey.50' }}>
                        <CardContent>
                          <Typography variant="caption" color="text.secondary">
                            {new Date(pred.date).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                          </Typography>
                          <Typography variant="h5" sx={{ fontWeight: 600, color: 'primary.main' }}>
                            {formatCurrency(pred.predicted_amount)}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Predicted expenses
                          </Typography>
                        </CardContent>
                      </Card>
                    ))}
                  </Stack>
                </>
              ) : (
                <Alert severity="info">
                  Insufficient transaction data to generate expense predictions. Add more transactions to enable AI forecasting.
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Warning Messages */}
          {riskData && riskData.score >= 50 && (
            <Alert severity="warning" icon={<Warning />}>
              <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                Action Required
              </Typography>
              <Typography variant="body2">
                Your risk score indicates potential financial stress. Consider reviewing your spending patterns,
                increasing your savings rate, and setting up budgets to better manage your expenses.
                Visit the Budget Control page for personalized recommendations.
              </Typography>
            </Alert>
          )}
        </Stack>
      </Container>
    </DashboardLayout>
  );
}

export default RiskPrediction;
