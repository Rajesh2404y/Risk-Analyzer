import { useEffect, useState, useCallback } from 'react';
import {
  Container,
  Box,
  Typography,
  Card,
  CardContent,
  CircularProgress,
  Stack,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Chip,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  CompareArrows,
  PieChart as PieChartIcon,
  EmojiEvents,
} from '@mui/icons-material';
import { LineChart } from '@mui/x-charts/LineChart';
import { PieChart } from '@mui/x-charts/PieChart';
import { BarChart } from '@mui/x-charts/BarChart';
import { analyticsAPI } from '../services/api';
import DashboardLayout from '../components/DashboardLayout';

interface Summary {
  total_income: number;
  total_expenses: number;
  net_savings: number;
  transaction_count: number;
  period: {
    start_date: string;
    end_date: string;
  };
}

interface TrendData {
  income: Array<{ period: string; amount: number }>;
  expenses: Array<{ period: string; amount: number }>;
}

interface CategoryBreakdown {
  category_id: number;
  category_name: string;
  color: string;
  amount: number;
  percentage: number;
  transaction_count: number;
}

interface Comparison {
  current_period: { start: string; end: string; total: number };
  previous_period: { start: string; end: string; total: number };
  change: number;
  change_percentage: number;
}

function Analytics() {
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [trends, setTrends] = useState<TrendData | null>(null);
  const [categoryBreakdown, setCategoryBreakdown] = useState<CategoryBreakdown[]>([]);
  const [comparison, setComparison] = useState<Comparison | null>(null);
  const [trendPeriod, setTrendPeriod] = useState('monthly');
  const [trendMonths, setTrendMonths] = useState(6);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [summaryRes, trendsRes, breakdownRes, comparisonRes] = await Promise.all([
        analyticsAPI.getSummary(),
        analyticsAPI.getTrends({ period: trendPeriod, months: trendMonths }),
        analyticsAPI.getCategoryBreakdown(),
        analyticsAPI.getComparison(),
      ]);

      setSummary(summaryRes.data.summary);
      setTrends(trendsRes.data.trends);
      setCategoryBreakdown(breakdownRes.data.breakdown || []);
      setComparison(comparisonRes.data.comparison);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  }, [trendPeriod, trendMonths]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const formatCurrency = (value: number) => `$${value.toFixed(2)}`;

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  };

  const pieData = categoryBreakdown.map((cat, index) => ({
    id: index,
    value: cat.amount,
    label: cat.category_name,
    color: cat.color,
  }));

  const getChangeColor = (change: number) => {
    return change <= 0 ? 'success' : 'error';
  };

  // Get top 3 spending categories
  const top3Categories = [...categoryBreakdown]
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 3);

  if (loading) {
    return (
      <DashboardLayout title="Expense Pattern Analysis">
        <Container maxWidth="xl" className="py-8">
          <Box className="flex justify-center items-center" sx={{ minHeight: '400px' }}>
            <CircularProgress />
          </Box>
        </Container>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Expense Pattern Analysis">
      <Container maxWidth="xl" className="py-8">
        <Stack spacing={3}>
          {/* Header */}
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 600 }}>
              Expense Pattern Analysis
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Analyze your spending patterns, trends, and category distribution
            </Typography>
          </Box>

        {/* Summary Cards */}
        <Stack direction={{ xs: 'column', md: 'row' }} spacing={3}>
          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography color="text.secondary" variant="body2">Total Income</Typography>
                  <Typography variant="h4" sx={{ fontWeight: 600, color: 'success.main' }}>
                    {formatCurrency(summary?.total_income || 0)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {summary?.period?.start_date && formatDate(summary.period.start_date)} - {summary?.period?.end_date && formatDate(summary.period.end_date)}
                  </Typography>
                </Box>
                <TrendingUp sx={{ fontSize: 48, color: 'success.main' }} />
              </Stack>
            </CardContent>
          </Card>

          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography color="text.secondary" variant="body2">Total Expenses</Typography>
                  <Typography variant="h4" sx={{ fontWeight: 600, color: 'error.main' }}>
                    {formatCurrency(summary?.total_expenses || 0)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {summary?.transaction_count || 0} transactions
                  </Typography>
                </Box>
                <TrendingDown sx={{ fontSize: 48, color: 'error.main' }} />
              </Stack>
            </CardContent>
          </Card>

          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography color="text.secondary" variant="body2">Net Savings</Typography>
                  <Typography 
                    variant="h4" 
                    sx={{ 
                      fontWeight: 600, 
                      color: (summary?.net_savings || 0) >= 0 ? 'success.main' : 'error.main' 
                    }}
                  >
                    {formatCurrency(summary?.net_savings || 0)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {((summary?.net_savings || 0) / (summary?.total_income || 1) * 100).toFixed(1)}% savings rate
                  </Typography>
                </Box>
                <CompareArrows sx={{ fontSize: 48, color: 'primary.main' }} />
              </Stack>
            </CardContent>
          </Card>
        </Stack>

        {/* Top 3 Spending Categories */}
        {top3Categories.length > 0 && (
          <Card sx={{ backgroundColor: 'primary.50' }}>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={1} className="mb-3">
                <EmojiEvents color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Top 3 Spending Categories
                </Typography>
              </Stack>
              <Stack direction={{ xs: 'column', md: 'row' }} spacing={3}>
                {top3Categories.map((cat, index) => (
                  <Card key={cat.category_id} variant="outlined" sx={{ flex: 1 }}>
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={2}>
                        <Box
                          sx={{
                            width: 48,
                            height: 48,
                            borderRadius: '50%',
                            backgroundColor: cat.color,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'white',
                            fontWeight: 700,
                            fontSize: '1.25rem',
                          }}
                        >
                          #{index + 1}
                        </Box>
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                            {cat.category_name}
                          </Typography>
                          <Typography variant="h5" sx={{ fontWeight: 700, color: cat.color }}>
                            {formatCurrency(cat.amount)}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {cat.percentage.toFixed(1)}% of total • {cat.transaction_count} transactions
                          </Typography>
                        </Box>
                      </Stack>
                    </CardContent>
                  </Card>
                ))}
              </Stack>
            </CardContent>
          </Card>
        )}

        {/* Month over Month Comparison */}
        {comparison && (
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                Month-over-Month Comparison
              </Typography>
              <Stack direction={{ xs: 'column', md: 'row' }} spacing={4} alignItems="center">
                <Box sx={{ flex: 1 }}>
                  <Typography color="text.secondary" variant="body2">Previous Month</Typography>
                  <Typography variant="h5" sx={{ fontWeight: 600 }}>
                    {formatCurrency(comparison.previous_period.total)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {formatDate(comparison.previous_period.start)} - {formatDate(comparison.previous_period.end)}
                  </Typography>
                </Box>
                
                <Box sx={{ textAlign: 'center' }}>
                  <Chip
                    icon={comparison.change <= 0 ? <TrendingDown /> : <TrendingUp />}
                    label={`${comparison.change_percentage >= 0 ? '+' : ''}${comparison.change_percentage.toFixed(1)}%`}
                    color={getChangeColor(comparison.change)}
                    sx={{ fontSize: '1rem', py: 2, px: 1 }}
                  />
                  <Typography variant="body2" color="text.secondary" className="mt-1">
                    {comparison.change <= 0 ? 'Decreased' : 'Increased'} by {formatCurrency(Math.abs(comparison.change))}
                  </Typography>
                </Box>

                <Box sx={{ flex: 1, textAlign: 'right' }}>
                  <Typography color="text.secondary" variant="body2">Current Month</Typography>
                  <Typography variant="h5" sx={{ fontWeight: 600 }}>
                    {formatCurrency(comparison.current_period.total)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {formatDate(comparison.current_period.start)} - {formatDate(comparison.current_period.end)}
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        )}

        {/* Trends Chart */}
        <Card>
          <CardContent>
            <Stack direction="row" justifyContent="space-between" alignItems="center" className="mb-4">
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Income & Expense Trends
              </Typography>
              <Stack direction="row" spacing={2}>
                <FormControl size="small" sx={{ minWidth: 120 }}>
                  <InputLabel>Period</InputLabel>
                  <Select
                    value={trendPeriod}
                    label="Period"
                    onChange={(e) => setTrendPeriod(e.target.value)}
                  >
                    <MenuItem value="daily">Daily</MenuItem>
                    <MenuItem value="weekly">Weekly</MenuItem>
                    <MenuItem value="monthly">Monthly</MenuItem>
                  </Select>
                </FormControl>
                <FormControl size="small" sx={{ minWidth: 100 }}>
                  <InputLabel>Months</InputLabel>
                  <Select
                    value={trendMonths}
                    label="Months"
                    onChange={(e) => setTrendMonths(Number(e.target.value))}
                  >
                    <MenuItem value={3}>3 Months</MenuItem>
                    <MenuItem value={6}>6 Months</MenuItem>
                    <MenuItem value={12}>12 Months</MenuItem>
                  </Select>
                </FormControl>
              </Stack>
            </Stack>

            {trends && (trends.income.length > 0 || trends.expenses.length > 0) ? (
              <LineChart
                xAxis={[
                  {
                    data: trends.expenses.map((_, i) => i),
                    scaleType: 'point',
                    valueFormatter: (value) => {
                      const item = trends.expenses[value] || trends.income[value];
                      return item?.period ? formatDate(item.period) : '';
                    },
                  },
                ]}
                series={[
                  {
                    data: trends.income.map(t => t.amount),
                    label: 'Income',
                    color: '#4caf50',
                    showMark: true,
                  },
                  {
                    data: trends.expenses.map(t => t.amount),
                    label: 'Expenses',
                    color: '#f44336',
                    showMark: true,
                  },
                ]}
                height={350}
              />
            ) : (
              <Alert severity="info">No trend data available. Add some transactions to see trends.</Alert>
            )}
          </CardContent>
        </Card>

        {/* Category Breakdown */}
        <Stack direction={{ xs: 'column', lg: 'row' }} spacing={3}>
          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={1} className="mb-4">
                <PieChartIcon color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Expense by Category
                </Typography>
              </Stack>

              {pieData.length > 0 ? (
                <PieChart
                  series={[
                    {
                      data: pieData,
                      highlightScope: { fade: 'global', highlight: 'item' },
                      faded: { innerRadius: 30, additionalRadius: -30 },
                      innerRadius: 60,
                      paddingAngle: 2,
                      cornerRadius: 4,
                    },
                  ]}
                  height={300}
                />
              ) : (
                <Alert severity="info">No expense data to show breakdown.</Alert>
              )}
            </CardContent>
          </Card>

          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                Category Breakdown
              </Typography>

              {categoryBreakdown.length > 0 ? (
                <Stack spacing={2}>
                  {categoryBreakdown.map((cat) => (
                    <Box key={cat.category_id}>
                      <Stack direction="row" justifyContent="space-between" alignItems="center">
                        <Stack direction="row" alignItems="center" spacing={1}>
                          <Box
                            sx={{
                              width: 12,
                              height: 12,
                              borderRadius: '50%',
                              backgroundColor: cat.color,
                            }}
                          />
                          <Typography variant="body2">{cat.category_name}</Typography>
                        </Stack>
                        <Stack direction="row" alignItems="center" spacing={2}>
                          <Typography variant="body2" color="text.secondary">
                            {cat.transaction_count} txns
                          </Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600, minWidth: 80, textAlign: 'right' }}>
                            {formatCurrency(cat.amount)}
                          </Typography>
                          <Chip
                            label={`${cat.percentage.toFixed(1)}%`}
                            size="small"
                            sx={{ 
                              minWidth: 60,
                              backgroundColor: cat.color + '20',
                              color: cat.color,
                            }}
                          />
                        </Stack>
                      </Stack>
                      <Box
                        sx={{
                          mt: 1,
                          height: 4,
                          backgroundColor: 'grey.200',
                          borderRadius: 2,
                          overflow: 'hidden',
                        }}
                      >
                        <Box
                          sx={{
                            width: `${cat.percentage}%`,
                            height: '100%',
                            backgroundColor: cat.color,
                            borderRadius: 2,
                          }}
                        />
                      </Box>
                    </Box>
                  ))}
                </Stack>
              ) : (
                <Alert severity="info">No category data available.</Alert>
              )}
            </CardContent>
          </Card>
        </Stack>

        {/* Bar Chart Comparison */}
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
              Category Spending Comparison
            </Typography>

            {categoryBreakdown.length > 0 ? (
              <BarChart
                xAxis={[
                  {
                    scaleType: 'band',
                    data: categoryBreakdown.map(c => c.category_name),
                  },
                ]}
                series={[
                  {
                    data: categoryBreakdown.map(c => c.amount),
                    label: 'Amount',
                    color: '#1976d2',
                  },
                ]}
                height={300}
              />
            ) : (
              <Alert severity="info">No data available for comparison.</Alert>
            )}
          </CardContent>
        </Card>
      </Stack>
    </Container>
    </DashboardLayout>
  );
}

export default Analytics;
