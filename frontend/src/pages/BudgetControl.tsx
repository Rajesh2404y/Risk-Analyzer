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
  Button,
  LinearProgress,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Snackbar,
} from '@mui/material';
import {
  CheckCircle,
  Close,
  Add as AddIcon,
  Delete as DeleteIcon,
  TrendingDown,
  Lightbulb,
  Warning,
  Savings,
} from '@mui/icons-material';
import { recommendationsAPI, budgetsAPI, categoriesAPI, riskAPI } from '../services/api';
import DashboardLayout from '../components/DashboardLayout';

interface Recommendation {
  type: string;
  title: string;
  message: string;
  impact: string;
  priority: number;
  potential_savings?: number;
}

interface RecommendationWithState extends Recommendation {
  status: 'pending' | 'accepted' | 'ignored';
}

interface Budget {
  id: number;
  category_id: number;
  category_name: string;
  category_color: string;
  amount: number;
  spent: number;
  period: string;
}

interface Category {
  id: number;
  name: string;
  type: string;
  color: string;
}

interface RiskContext {
  score: number;
  level: string;
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
};

const getPriorityColor = (priority: number): 'error' | 'warning' | 'info' | 'success' => {
  if (priority >= 8) return 'error';
  if (priority >= 6) return 'warning';
  if (priority >= 4) return 'info';
  return 'success';
};

const getBudgetStatus = (spent: number, amount: number): { color: string; status: string } => {
  const percentage = (spent / amount) * 100;
  if (percentage >= 100) return { color: '#f44336', status: 'Over Budget' };
  if (percentage >= 80) return { color: '#ff9800', status: 'Near Limit' };
  if (percentage >= 50) return { color: '#2196f3', status: 'On Track' };
  return { color: '#4caf50', status: 'Under Budget' };
};

function BudgetControl() {
  const [loading, setLoading] = useState(true);
  const [recommendations, setRecommendations] = useState<RecommendationWithState[]>([]);
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [riskContext, setRiskContext] = useState<RiskContext | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [newBudget, setNewBudget] = useState({ category_id: '', amount: '' });
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' | 'info' });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      const [recRes, budgetsRes, categoriesRes, riskRes] = await Promise.all([
        recommendationsAPI.getRecommendations(),
        budgetsAPI.getBudgets(),
        categoriesAPI.getCategories(),
        riskAPI.getRiskScore(),
      ]);

      // Add status to recommendations
      const recsWithStatus = (recRes.data.recommendations || []).map((rec: Recommendation) => ({
        ...rec,
        status: 'pending' as const,
      }));
      setRecommendations(recsWithStatus);
      setBudgets(budgetsRes.data.budgets || []);
      setCategories(categoriesRes.data.categories?.filter((c: Category) => c.type === 'expense') || []);
      setRiskContext(recRes.data.risk_context || { score: riskRes.data.score, level: riskRes.data.risk_level });
    } catch (error) {
      console.error('Error loading data:', error);
      setSnackbar({ open: true, message: 'Failed to load data', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleAcceptRecommendation = (index: number) => {
    setRecommendations(prev =>
      prev.map((rec, i) => (i === index ? { ...rec, status: 'accepted' } : rec))
    );
    setSnackbar({
      open: true,
      message: 'Recommendation accepted! Tracking your progress.',
      severity: 'success',
    });
  };

  const handleIgnoreRecommendation = (index: number) => {
    setRecommendations(prev =>
      prev.map((rec, i) => (i === index ? { ...rec, status: 'ignored' } : rec))
    );
    setSnackbar({
      open: true,
      message: 'Recommendation ignored.',
      severity: 'info',
    });
  };

  const handleCreateBudget = async () => {
    if (!newBudget.category_id || !newBudget.amount) {
      setSnackbar({ open: true, message: 'Please fill all fields', severity: 'error' });
      return;
    }

    try {
      await budgetsAPI.createBudget({
        category_id: parseInt(newBudget.category_id),
        amount: parseFloat(newBudget.amount),
        period: 'monthly',
      });

      setDialogOpen(false);
      setNewBudget({ category_id: '', amount: '' });
      setSnackbar({ open: true, message: 'Budget created successfully!', severity: 'success' });
      loadData();
    } catch (error) {
      console.error('Error creating budget:', error);
      setSnackbar({ open: true, message: 'Failed to create budget', severity: 'error' });
    }
  };

  const handleDeleteBudget = async (id: number) => {
    try {
      await budgetsAPI.deleteBudget(id);
      setSnackbar({ open: true, message: 'Budget deleted successfully', severity: 'success' });
      loadData();
    } catch (error) {
      console.error('Error deleting budget:', error);
      setSnackbar({ open: true, message: 'Failed to delete budget', severity: 'error' });
    }
  };

  const pendingRecommendations = recommendations.filter(r => r.status === 'pending');
  const acceptedRecommendations = recommendations.filter(r => r.status === 'accepted');
  const totalPotentialSavings = pendingRecommendations.reduce((sum, r) => sum + (r.potential_savings || 0), 0);
  const acceptedSavings = acceptedRecommendations.reduce((sum, r) => sum + (r.potential_savings || 0), 0);

  // Calculate expected risk reduction based on accepted recommendations
  const calculateRiskReduction = (): number => {
    if (recommendations.length === 0) return 0;

    // Simple heuristic: each accepted recommendation reduces risk by ~3-5 points
    const avgReduction = acceptedRecommendations.reduce((sum, r) => {
      if (r.priority >= 8) return sum + 5;
      if (r.priority >= 6) return sum + 4;
      return sum + 3;
    }, 0);

    return Math.min(avgReduction, riskContext?.score || 0);
  };

  const expectedRiskReduction = calculateRiskReduction();
  const projectedRiskScore = Math.max(0, (riskContext?.score || 0) - expectedRiskReduction);

  if (loading) {
    return (
      <DashboardLayout title="Budget Control">
        <Container maxWidth="xl" className="py-8">
          <Box className="flex justify-center items-center" sx={{ minHeight: '400px' }}>
            <CircularProgress />
          </Box>
        </Container>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Budget Control">
      <Container maxWidth="xl" className="py-8">
        <Stack spacing={3}>
          {/* Header */}
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="h4" sx={{ fontWeight: 600 }}>
                Recommendation & Budget Control
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Take action on AI recommendations and manage your budgets
              </Typography>
            </Box>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setDialogOpen(true)}
            >
              Add Budget
            </Button>
          </Stack>

          {/* Summary Cards */}
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={3}>
            {/* Current Risk */}
            <Card sx={{ flex: 1 }}>
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                  <Box>
                    <Typography variant="body2" color="text.secondary">Current Risk Score</Typography>
                    <Typography variant="h4" sx={{ fontWeight: 600 }}>
                      {riskContext?.score || 0}/100
                    </Typography>
                    <Chip
                      label={riskContext?.level?.toUpperCase() || 'N/A'}
                      color={riskContext?.level === 'low' ? 'success' : riskContext?.level === 'medium' ? 'warning' : 'error'}
                      size="small"
                      sx={{ mt: 1 }}
                    />
                  </Box>
                  <Warning sx={{ fontSize: 48, color: riskContext?.level === 'low' ? 'success.main' : riskContext?.level === 'medium' ? 'warning.main' : 'error.main' }} />
                </Stack>
              </CardContent>
            </Card>

            {/* Expected Risk Reduction */}
            <Card sx={{ flex: 1, backgroundColor: 'success.50' }}>
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                  <Box>
                    <Typography variant="body2" color="text.secondary">Expected Risk Reduction</Typography>
                    <Typography variant="h4" sx={{ fontWeight: 600, color: 'success.main' }}>
                      -{expectedRiskReduction} pts
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Projected score: {projectedRiskScore}/100
                    </Typography>
                  </Box>
                  <TrendingDown sx={{ fontSize: 48, color: 'success.main' }} />
                </Stack>
              </CardContent>
            </Card>

            {/* Potential Savings */}
            <Card sx={{ flex: 1 }}>
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                  <Box>
                    <Typography variant="body2" color="text.secondary">Potential Savings</Typography>
                    <Typography variant="h4" sx={{ fontWeight: 600, color: 'primary.main' }}>
                      {formatCurrency(totalPotentialSavings + acceptedSavings)}
                    </Typography>
                    <Typography variant="caption" color="success.main">
                      {formatCurrency(acceptedSavings)} accepted
                    </Typography>
                  </Box>
                  <Savings sx={{ fontSize: 48, color: 'primary.main' }} />
                </Stack>
              </CardContent>
            </Card>
          </Stack>

          {/* AI Recommendations */}
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={1} className="mb-4">
                <Lightbulb color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  AI Recommendations
                </Typography>
                <Chip label={`${pendingRecommendations.length} pending`} size="small" color="primary" variant="outlined" />
              </Stack>

              {recommendations.length === 0 ? (
                <Alert severity="success" icon={<CheckCircle />}>
                  Great job! No recommendations at this time. Your finances are on track!
                </Alert>
              ) : (
                <Stack spacing={2}>
                  {recommendations.map((rec, index) => (
                    <Card
                      key={index}
                      variant="outlined"
                      sx={{
                        opacity: rec.status === 'ignored' ? 0.5 : 1,
                        backgroundColor: rec.status === 'accepted' ? 'success.50' : 'background.paper',
                        borderColor: rec.status === 'accepted' ? 'success.main' : 'divider',
                      }}
                    >
                      <CardContent>
                        <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} alignItems={{ md: 'center' }}>
                          <Box sx={{ flex: 1 }}>
                            <Stack direction="row" alignItems="center" spacing={1} className="mb-1">
                              <Chip
                                label={`Priority ${rec.priority}`}
                                size="small"
                                color={getPriorityColor(rec.priority)}
                              />
                              {rec.status === 'accepted' && (
                                <Chip label="Accepted" size="small" color="success" icon={<CheckCircle />} />
                              )}
                              {rec.status === 'ignored' && (
                                <Chip label="Ignored" size="small" variant="outlined" />
                              )}
                            </Stack>
                            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                              {rec.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary" className="mb-1">
                              {rec.message}
                            </Typography>
                            <Stack direction="row" spacing={2}>
                              <Typography variant="caption" color="text.secondary">
                                Impact: <strong>{rec.impact}</strong>
                              </Typography>
                              {rec.potential_savings && rec.potential_savings > 0 && (
                                <Typography variant="caption" color="success.main" sx={{ fontWeight: 600 }}>
                                  Potential savings: {formatCurrency(rec.potential_savings)}
                                </Typography>
                              )}
                            </Stack>
                          </Box>

                          {rec.status === 'pending' && (
                            <Stack direction="row" spacing={1}>
                              <Button
                                variant="contained"
                                color="success"
                                size="small"
                                startIcon={<CheckCircle />}
                                onClick={() => handleAcceptRecommendation(index)}
                              >
                                Accept
                              </Button>
                              <Button
                                variant="outlined"
                                color="inherit"
                                size="small"
                                startIcon={<Close />}
                                onClick={() => handleIgnoreRecommendation(index)}
                              >
                                Ignore
                              </Button>
                            </Stack>
                          )}
                        </Stack>
                      </CardContent>
                    </Card>
                  ))}
                </Stack>
              )}
            </CardContent>
          </Card>

          {/* Budget Progress */}
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Budget Progress
              </Typography>

              {budgets.length === 0 ? (
                <Alert severity="info">
                  No budgets set up yet. Create budgets to track your spending against limits.
                </Alert>
              ) : (
                <Stack spacing={3}>
                  {budgets.map((budget) => {
                    const percentage = Math.min((budget.spent / budget.amount) * 100, 100);
                    const { color, status } = getBudgetStatus(budget.spent, budget.amount);

                    return (
                      <Box key={budget.id}>
                        <Stack direction="row" justifyContent="space-between" alignItems="center" className="mb-2">
                          <Stack direction="row" alignItems="center" spacing={2}>
                            <Box
                              sx={{
                                width: 16,
                                height: 16,
                                borderRadius: '50%',
                                backgroundColor: budget.category_color || '#1976d2',
                              }}
                            />
                            <Typography sx={{ fontWeight: 500 }}>
                              {budget.category_name}
                            </Typography>
                            <Chip
                              label={status}
                              size="small"
                              sx={{
                                backgroundColor: `${color}20`,
                                color: color,
                                fontWeight: 600,
                              }}
                            />
                          </Stack>
                          <Stack direction="row" alignItems="center" spacing={2}>
                            <Typography variant="body2">
                              <strong>{formatCurrency(budget.spent)}</strong> / {formatCurrency(budget.amount)}
                            </Typography>
                            <Tooltip title="Delete budget">
                              <IconButton
                                size="small"
                                color="error"
                                onClick={() => handleDeleteBudget(budget.id)}
                              >
                                <DeleteIcon fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          </Stack>
                        </Stack>
                        <LinearProgress
                          variant="determinate"
                          value={percentage}
                          sx={{
                            height: 12,
                            borderRadius: 6,
                            backgroundColor: '#e0e0e0',
                            '& .MuiLinearProgress-bar': {
                              backgroundColor: color,
                              borderRadius: 6,
                            },
                          }}
                        />
                        <Typography variant="caption" color="text.secondary" className="mt-1">
                          {percentage.toFixed(0)}% used • {formatCurrency(Math.max(0, budget.amount - budget.spent))} remaining
                        </Typography>
                      </Box>
                    );
                  })}
                </Stack>
              )}
            </CardContent>
          </Card>
        </Stack>

        {/* Add Budget Dialog */}
        <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
          <DialogTitle>Create New Budget</DialogTitle>
          <DialogContent>
            <Stack spacing={3} className="mt-2">
              <FormControl fullWidth>
                <InputLabel>Category</InputLabel>
                <Select
                  value={newBudget.category_id}
                  label="Category"
                  onChange={(e) => setNewBudget({ ...newBudget, category_id: e.target.value })}
                >
                  {categories
                    .filter(cat => !budgets.some(b => b.category_id === cat.id))
                    .map((cat) => (
                      <MenuItem key={cat.id} value={cat.id.toString()}>
                        <Stack direction="row" alignItems="center" spacing={1}>
                          <Box
                            sx={{
                              width: 12,
                              height: 12,
                              borderRadius: '50%',
                              backgroundColor: cat.color,
                            }}
                          />
                          <span>{cat.name}</span>
                        </Stack>
                      </MenuItem>
                    ))}
                </Select>
              </FormControl>

              <TextField
                label="Monthly Budget Amount"
                type="number"
                value={newBudget.amount}
                onChange={(e) => setNewBudget({ ...newBudget, amount: e.target.value })}
                fullWidth
                slotProps={{
                  input: { startAdornment: <Typography sx={{ mr: 1 }}>$</Typography> },
                }}
              />
            </Stack>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
            <Button variant="contained" onClick={handleCreateBudget}>
              Create Budget
            </Button>
          </DialogActions>
        </Dialog>

        {/* Snackbar */}
        <Snackbar
          open={snackbar.open}
          autoHideDuration={4000}
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
          <Alert
            onClose={() => setSnackbar({ ...snackbar, open: false })}
            severity={snackbar.severity}
            variant="filled"
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Container>
    </DashboardLayout>
  );
}

export default BudgetControl;
