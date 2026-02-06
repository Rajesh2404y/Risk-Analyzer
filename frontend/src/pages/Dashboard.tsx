import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  CircularProgress,
  Alert,
  Stack,
  Chip,
  Snackbar,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  AccountBalance,
  Warning,
  Email as EmailIcon,
  ArrowForward,
} from '@mui/icons-material';
import { LineChart } from '@mui/x-charts/LineChart';
import { PieChart } from '@mui/x-charts/PieChart';
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
import { analyticsAPI, riskAPI, predictionsAPI, recommendationsAPI } from '../services/api';
import DashboardLayout from '../components/DashboardLayout';

interface Summary {
  total_income: number;
  total_expenses: number;
  net_savings: number;
}

interface TrendData {
  month: string;
  income: number;
  expenses: number;
}

interface RiskData {
  score: number;
  risk_level: string;
}

interface Recommendation {
  type: string;
  title: string;
  message: string;
  impact: string;
  priority: number;
}

function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [riskData, setRiskData] = useState<RiskData | null>(null);
  const [predictions, setPredictions] = useState<Array<{ date: string; predicted_amount: number }>>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [categoryData, setCategoryData] = useState<Array<{ label: string; value: number; id: number }>>([]);
  const [trendData, setTrendData] = useState<TrendData[]>([]);
  const [sendingEmail, setSendingEmail] = useState(false);
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' | 'info' }>({
    open: false,
    message: '',
    severity: 'info',
  });
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch all dashboard data
      const [summaryRes, riskRes, predictionsRes, recommendationsRes, categoryRes, trendsRes] = await Promise.all([
        analyticsAPI.getSummary(),
        riskAPI.getRiskScore(),
        predictionsAPI.getPredictions(3),
        recommendationsAPI.getRecommendations(),
        analyticsAPI.getCategoryBreakdown(),
        analyticsAPI.getTrends(),
      ]);

      setSummary(summaryRes.data.summary);
      setRiskData(riskRes.data);
      setPredictions(predictionsRes.data.predictions || []);
      setRecommendations(recommendationsRes.data.recommendations || []);
      
      // Format category data for pie chart
      const categories = categoryRes.data.breakdown || [];
      setCategoryData(categories.map((cat: { category_name: string; amount: number; category_id: number }) => ({
        label: cat.category_name,
        value: cat.amount,
        id: cat.category_id,
      })));
      
      // Format trend data
      const trends = trendsRes.data.trends || [];
      setTrendData(trends);
      
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendAlertEmail = async () => {
    try {
      setSendingEmail(true);
      const response = await recommendationsAPI.sendAlertEmail();
      
      if (response.data.sent) {
        setSnackbar({
          open: true,
          message: response.data.message || 'Alert email sent successfully!',
          severity: 'success',
        });
      } else {
        setSnackbar({
          open: true,
          message: response.data.message || response.data.error || 'Could not send email',
          severity: 'info',
        });
      }
    } catch (error: unknown) {
      let errorMessage = 'Failed to send alert email';
      
      if (error && typeof error === 'object' && 'response' in error) {
        const response = (error as { response?: { data?: { error?: string; configuration_help?: unknown } } }).response;
        if (response?.data?.error) {
          errorMessage = response.data.error;
          
          // If it's a configuration error, show helpful message
          if (response.data.configuration_help) {
            errorMessage += '\n\nPlease check the EMAIL_SETUP.md file for configuration instructions.';
          }
        }
      }
      
      setSnackbar({
        open: true,
        message: errorMessage,
        severity: 'error',
      });
    } finally {
      setSendingEmail(false);
    }
  };

  const getRiskColor = (level: string): 'success' | 'warning' | 'error' | 'info' => {
    switch (level) {
      case 'low': return 'success';
      case 'medium': return 'warning';
      case 'high': return 'error';
      default: return 'info';
    }
  };

  const getGaugeColor = (score: number): string => {
    if (score < 35) return '#4caf50';
    if (score < 65) return '#ff9800';
    return '#f44336';
  };

  return (
    <DashboardLayout title="Smart Overview Dashboard">
      <Container maxWidth="xl" className="py-8">
        {loading ? (
          <Box className="flex justify-center items-center" sx={{ minHeight: '400px' }}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            {/* Summary Cards */}
            <Grid size={{ xs: 12, md: 4 }}>
              <Card>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography color="text.secondary" variant="body2">Total Income</Typography>
                      <Typography variant="h4" sx={{ fontWeight: 600, color: 'success.main' }}>
                        ${summary?.total_income.toFixed(2) || '0.00'}
                      </Typography>
                    </Box>
                    <TrendingUp sx={{ fontSize: 48, color: 'success.main' }} />
                  </Stack>
                </CardContent>
              </Card>
            </Grid>

            <Grid size={{ xs: 12, md: 4 }}>
              <Card>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography color="text.secondary" variant="body2">Total Expenses</Typography>
                      <Typography variant="h4" sx={{ fontWeight: 600, color: 'error.main' }}>
                        ${summary?.total_expenses.toFixed(2) || '0.00'}
                      </Typography>
                    </Box>
                    <TrendingDown sx={{ fontSize: 48, color: 'error.main' }} />
                  </Stack>
                </CardContent>
              </Card>
            </Grid>

            <Grid size={{ xs: 12, md: 4 }}>
              <Card>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography color="text.secondary" variant="body2">Net Savings</Typography>
                      <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
                        ${summary?.net_savings.toFixed(2) || '0.00'}
                      </Typography>
                    </Box>
                    <AccountBalance sx={{ fontSize: 48, color: 'primary.main' }} />
                  </Stack>
                </CardContent>
              </Card>
            </Grid>

            {/* Risk Score Card with Gauge */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Stack spacing={2}>
                    <Stack direction="row" justifyContent="space-between" alignItems="center">
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        Financial Risk Score
                      </Typography>
                    <Chip
                        label={riskData?.risk_level.toUpperCase() || 'N/A'}
                        color={getRiskColor(riskData?.risk_level || '')}
                        size="small"
                        sx={{ fontWeight: 600 }}
                      />
                    </Stack>
                    
                    <Box className="flex justify-center items-center" sx={{ height: 180 }}>
                      <Gauge
                        value={riskData?.score || 0}
                        valueMax={100}
                        startAngle={-110}
                        endAngle={110}
                        sx={{
                          width: 220,
                          height: 180,
                          [`& .${gaugeClasses.valueText}`]: {
                            fontSize: 36,
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
                    
                    <Alert 
                      severity={getRiskColor(riskData?.risk_level || '')} 
                      icon={<Warning />}
                    >
                      {riskData?.risk_level === 'low' && 'Great! Your finances are healthy.'}
                      {riskData?.risk_level === 'medium' && 'Your finances need some attention.'}
                      {riskData?.risk_level === 'high' && 'Critical: Take immediate action!'}
                      {!riskData?.risk_level && 'Add transactions to calculate risk.'}
                    </Alert>

                    <Button
                      variant="outlined"
                      size="small"
                      endIcon={<ArrowForward />}
                      onClick={() => navigate('/risk-predictions')}
                    >
                      View Detailed Analysis
                    </Button>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>

            {/* Category Breakdown */}
            <Grid size={{ xs: 12, md: 6 }}>
              <Card>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                    Expense Breakdown
                  </Typography>
                  {categoryData.length > 0 ? (
                    <PieChart
                      series={[
                        {
                          data: categoryData,
                          highlightScope: { fade: 'global', highlight: 'item' },
                          faded: { innerRadius: 30, additionalRadius: -30 },
                        },
                      ]}
                      height={250}
                    />
                  ) : (
                    <Typography color="text.secondary" className="text-center py-8">
                      No expense data available
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>

            {/* Monthly Trends */}
            <Grid size={{ xs: 12 }}>
              <Card>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                    Monthly Income vs Expenses Trend
                  </Typography>
                  {trendData.length > 0 ? (
                    <LineChart
                      xAxis={[
                        {
                          data: trendData.map((_, index) => index),
                          scaleType: 'point',
                          valueFormatter: (value) => trendData[value]?.month || '',
                        },
                      ]}
                      series={[
                        {
                          data: trendData.map(t => t.income),
                          label: 'Income',
                          color: '#4caf50',
                          showMark: true,
                        },
                        {
                          data: trendData.map(t => t.expenses),
                          label: 'Expenses',
                          color: '#f44336',
                          showMark: true,
                        },
                      ]}
                      height={300}
                    />
                  ) : (
                    <Typography color="text.secondary" className="text-center py-8">
                      No trend data available
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>

            {/* Expense Predictions */}
            <Grid size={{ xs: 12 }}>
              <Card>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                    AI-Powered Expense Predictions (Next 3 Months)
                  </Typography>
                  {predictions.length > 0 ? (
                    <LineChart
                      xAxis={[
                        {
                          data: predictions.map((_, index) => index),
                          scaleType: 'point',
                          valueFormatter: (value) => predictions[value]?.date?.substring(0, 7) || '',
                        },
                      ]}
                      series={[
                        {
                          data: predictions.map(p => p.predicted_amount),
                          label: 'Predicted Expenses',
                          area: true,
                          showMark: true,
                        },
                      ]}
                      height={300}
                    />
                  ) : (
                    <Typography color="text.secondary" className="text-center py-8">
                      Insufficient data for predictions
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>

            {/* Recommendations */}
            <Grid size={{ xs: 12 }}>
              <Card>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" className="mb-4">
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      AI Recommendations
                    </Typography>
                    {recommendations.length > 0 && (
                      <Button
                        variant="contained"
                        color="primary"
                        startIcon={sendingEmail ? <CircularProgress size={16} color="inherit" /> : <EmailIcon />}
                        onClick={handleSendAlertEmail}
                        disabled={sendingEmail}
                        size="small"
                      >
                        {sendingEmail ? 'Sending...' : 'Send Alert Email'}
                      </Button>
                    )}
                  </Stack>
                  {recommendations.length > 0 ? (
                    <Stack spacing={2}>
                      {recommendations.slice(0, 5).map((rec, index) => (
                        <Alert
                          key={index}
                          severity={rec.priority > 7 ? 'error' : rec.priority > 5 ? 'warning' : 'info'}
                        >
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            {rec.title}
                          </Typography>
                          <Typography variant="body2">{rec.message}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            Impact: {rec.impact}
                          </Typography>
                        </Alert>
                      ))}
                    </Stack>
                  ) : (
                    <Stack spacing={2}>
                      <Typography color="text.secondary">
                        No recommendations at this time. Keep tracking your expenses!
                      </Typography>
                      <Stack direction="row" spacing={2}>
                        <Button
                          variant="outlined"
                          color="primary"
                          startIcon={sendingEmail ? <CircularProgress size={16} color="inherit" /> : <EmailIcon />}
                          onClick={handleSendAlertEmail}
                          disabled={sendingEmail}
                          size="small"
                        >
                          {sendingEmail ? 'Sending...' : 'Test Email Alert'}
                        </Button>
                        <Button
                          variant="text"
                          size="small"
                          onClick={() => navigate('/budget-control')}
                        >
                          Manage Budgets
                        </Button>
                      </Stack>
                    </Stack>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </Container>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={() => setSnackbar({ ...snackbar, open: false })} 
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </DashboardLayout>
  );
}

export default Dashboard;
