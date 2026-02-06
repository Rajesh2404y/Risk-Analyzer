import { useEffect, useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Stack,
  CircularProgress,
  Alert,
  InputAdornment,
  FormControlLabel,
  Switch,
  Snackbar,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  TrendingUp,
  TrendingDown,
  FilterList as FilterIcon,
  Search as SearchIcon,
  CloudUpload as UploadIcon,
} from '@mui/icons-material';
import { transactionsAPI, categoriesAPI } from '../services/api';
import FileUpload from '../components/FileUpload';
import DashboardLayout from '../components/DashboardLayout';

interface Category {
  id: number;
  name: string;
  type: string;
  icon: string;
  color: string;
}

interface Transaction {
  id: number;
  type: 'income' | 'expense';
  amount: number;
  category: Category | null;
  description: string;
  transaction_date: string;
  merchant: string;
  payment_method: string;
  is_recurring: boolean;
}

interface TransactionForm {
  type: 'income' | 'expense';
  amount: string;
  category_id: string;
  description: string;
  transaction_date: string;
  merchant: string;
  payment_method: string;
  is_recurring: boolean;
}

const initialForm: TransactionForm = {
  type: 'expense',
  amount: '',
  category_id: '',
  description: '',
  transaction_date: new Date().toISOString().split('T')[0],
  merchant: '',
  payment_method: 'card',
  is_recurring: false,
};

function Transactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<TransactionForm>(initialForm);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [transactionsRes, categoriesRes] = await Promise.all([
        transactionsAPI.getTransactions(),
        categoriesAPI.getCategories(),
      ]);
      setTransactions(transactionsRes.data.transactions || []);
      setCategories(categoriesRes.data.categories || []);
    } catch (error) {
      console.error('Error loading data:', error);
      setSnackbar({ open: true, message: 'Failed to load transactions', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (transaction?: Transaction) => {
    if (transaction) {
      setEditingId(transaction.id);
      setForm({
        type: transaction.type,
        amount: transaction.amount.toString(),
        category_id: transaction.category?.id.toString() || '',
        description: transaction.description || '',
        transaction_date: transaction.transaction_date,
        merchant: transaction.merchant || '',
        payment_method: transaction.payment_method || 'card',
        is_recurring: transaction.is_recurring,
      });
    } else {
      setEditingId(null);
      setForm(initialForm);
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingId(null);
    setForm(initialForm);
  };

  const handleSubmit = async () => {
    try {
      const data = {
        type: form.type,
        amount: parseFloat(form.amount),
        category_id: form.category_id ? parseInt(form.category_id) : null,
        description: form.description,
        transaction_date: form.transaction_date,
        merchant: form.merchant,
        payment_method: form.payment_method,
        is_recurring: form.is_recurring,
      };

      if (editingId) {
        await transactionsAPI.updateTransaction(editingId, data);
        setSnackbar({ open: true, message: 'Transaction updated successfully', severity: 'success' });
      } else {
        await transactionsAPI.createTransaction(data);
        setSnackbar({ open: true, message: 'Transaction created successfully', severity: 'success' });
      }

      handleCloseDialog();
      loadData();
    } catch (error) {
      console.error('Error saving transaction:', error);
      setSnackbar({ open: true, message: 'Failed to save transaction', severity: 'error' });
    }
  };

  const handleDelete = async () => {
    if (!deletingId) return;
    
    try {
      await transactionsAPI.deleteTransaction(deletingId);
      setSnackbar({ open: true, message: 'Transaction deleted successfully', severity: 'success' });
      setDeleteDialogOpen(false);
      setDeletingId(null);
      loadData();
    } catch (error) {
      console.error('Error deleting transaction:', error);
      setSnackbar({ open: true, message: 'Failed to delete transaction', severity: 'error' });
    }
  };

  const filteredTransactions = transactions.filter((t) => {
    const matchesSearch = 
      t.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.merchant?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.category?.name?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = filterType === 'all' || t.type === filterType;
    return matchesSearch && matchesType;
  });

  const filteredCategories = categories.filter((c) => c.type === form.type);

  const totalIncome = transactions.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0);
  const totalExpenses = transactions.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);

  return (
    <DashboardLayout title="Transaction Upload & History">
      <Container maxWidth="xl" className="py-8">
        <Stack spacing={3}>
          {/* Header */}
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="h4" sx={{ fontWeight: 600 }}>
                Transaction Upload & History
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Upload bank statements and manage your transaction history
              </Typography>
            </Box>
          <Stack direction="row" spacing={2}>
            <Button
              variant="outlined"
              startIcon={<UploadIcon />}
              onClick={() => setActiveTab(1)}
            >
              Import Statement
            </Button>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => handleOpenDialog()}
            >
              Add Transaction
            </Button>
          </Stack>
        </Stack>

        {/* Tabs */}
        <Card>
          <Tabs 
            value={activeTab} 
            onChange={(_, newValue) => setActiveTab(newValue)}
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
            <Tab label="All Transactions" />
            <Tab label="Import from File" icon={<UploadIcon />} iconPosition="start" />
          </Tabs>
        </Card>

        {/* Tab Content */}
        {activeTab === 1 ? (
          <FileUpload 
            onTransactionsImported={() => {
              loadData();
              setActiveTab(0);
              setSnackbar({ 
                open: true, 
                message: 'Transactions imported successfully!', 
                severity: 'success' 
              });
            }} 
          />
        ) : (
          <>
            {/* Summary Cards */}
            <Stack direction={{ xs: 'column', md: 'row' }} spacing={3}>
              <Card sx={{ flex: 1 }}>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography color="text.secondary" variant="body2">Total Income</Typography>
                      <Typography variant="h5" sx={{ fontWeight: 600, color: 'success.main' }}>
                        ${totalIncome.toFixed(2)}
                      </Typography>
                    </Box>
                    <TrendingUp sx={{ fontSize: 40, color: 'success.main' }} />
                  </Stack>
                </CardContent>
              </Card>

              <Card sx={{ flex: 1 }}>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography color="text.secondary" variant="body2">Total Expenses</Typography>
                      <Typography variant="h5" sx={{ fontWeight: 600, color: 'error.main' }}>
                        ${totalExpenses.toFixed(2)}
                      </Typography>
                    </Box>
                    <TrendingDown sx={{ fontSize: 40, color: 'error.main' }} />
                  </Stack>
                </CardContent>
              </Card>

              <Card sx={{ flex: 1 }}>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography color="text.secondary" variant="body2">Net Balance</Typography>
                      <Typography 
                        variant="h5" 
                        sx={{ fontWeight: 600, color: totalIncome - totalExpenses >= 0 ? 'success.main' : 'error.main' }}
                      >
                        ${(totalIncome - totalExpenses).toFixed(2)}
                      </Typography>
                    </Box>
                    <FilterIcon sx={{ fontSize: 40, color: 'primary.main' }} />
                  </Stack>
                </CardContent>
              </Card>
            </Stack>

            {/* Filters */}
        <Card>
          <CardContent>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} alignItems="center">
              <TextField
                size="small"
                placeholder="Search transactions..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
                sx={{ minWidth: 250 }}
              />
              <FormControl size="small" sx={{ minWidth: 150 }}>
                <InputLabel>Type</InputLabel>
                <Select
                  value={filterType}
                  label="Type"
                  onChange={(e) => setFilterType(e.target.value)}
                >
                  <MenuItem value="all">All</MenuItem>
                  <MenuItem value="income">Income</MenuItem>
                  <MenuItem value="expense">Expense</MenuItem>
                </Select>
              </FormControl>
              <Typography variant="body2" color="text.secondary" sx={{ ml: 'auto' }}>
                Showing {filteredTransactions.length} of {transactions.length} transactions
              </Typography>
            </Stack>
          </CardContent>
        </Card>

        {/* Transactions Table */}
        <Card>
          <TableContainer component={Paper} elevation={0}>
            {loading ? (
              <Box className="flex justify-center items-center py-16">
                <CircularProgress />
              </Box>
            ) : filteredTransactions.length === 0 ? (
              <Box className="text-center py-16">
                <Typography color="text.secondary">No transactions found</Typography>
                <Button
                  variant="outlined"
                  startIcon={<AddIcon />}
                  onClick={() => handleOpenDialog()}
                  className="mt-4"
                >
                  Add Your First Transaction
                </Button>
              </Box>
            ) : (
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>Description</TableCell>
                    <TableCell>Category</TableCell>
                    <TableCell>Merchant</TableCell>
                    <TableCell align="right">Amount</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell align="center">Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {filteredTransactions.map((transaction) => (
                    <TableRow key={transaction.id} hover>
                      <TableCell>
                        {new Date(transaction.transaction_date).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <Stack direction="row" alignItems="center" spacing={1}>
                          <Typography variant="body2">{transaction.description || '-'}</Typography>
                          {transaction.is_recurring && (
                            <Chip label="Recurring" size="small" variant="outlined" />
                          )}
                        </Stack>
                      </TableCell>
                      <TableCell>
                        {transaction.category ? (
                          <Chip
                            label={transaction.category.name}
                            size="small"
                            sx={{ 
                              backgroundColor: transaction.category.color + '20',
                              color: transaction.category.color,
                              borderColor: transaction.category.color,
                            }}
                            variant="outlined"
                          />
                        ) : (
                          '-'
                        )}
                      </TableCell>
                      <TableCell>{transaction.merchant || '-'}</TableCell>
                      <TableCell align="right">
                        <Typography
                          sx={{
                            fontWeight: 600,
                            color: transaction.type === 'income' ? 'success.main' : 'error.main',
                          }}
                        >
                          {transaction.type === 'income' ? '+' : '-'}${transaction.amount.toFixed(2)}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={transaction.type}
                          size="small"
                          color={transaction.type === 'income' ? 'success' : 'error'}
                        />
                      </TableCell>
                      <TableCell align="center">
                        <IconButton size="small" onClick={() => handleOpenDialog(transaction)}>
                          <EditIcon fontSize="small" />
                        </IconButton>
                        <IconButton 
                          size="small" 
                          color="error"
                          onClick={() => {
                            setDeletingId(transaction.id);
                            setDeleteDialogOpen(true);
                          }}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </TableContainer>
        </Card>
        </>
        )}
      </Stack>

      {/* Add/Edit Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>{editingId ? 'Edit Transaction' : 'Add Transaction'}</DialogTitle>
        <DialogContent>
          <Stack spacing={3} className="mt-2">
            <FormControl fullWidth>
              <InputLabel>Type</InputLabel>
              <Select
                value={form.type}
                label="Type"
                onChange={(e) => setForm({ ...form, type: e.target.value as 'income' | 'expense', category_id: '' })}
              >
                <MenuItem value="income">Income</MenuItem>
                <MenuItem value="expense">Expense</MenuItem>
              </Select>
            </FormControl>

            <TextField
              label="Amount"
              type="number"
              value={form.amount}
              onChange={(e) => setForm({ ...form, amount: e.target.value })}
              InputProps={{
                startAdornment: <InputAdornment position="start">$</InputAdornment>,
              }}
              fullWidth
              required
            />

            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select
                value={form.category_id}
                label="Category"
                onChange={(e) => setForm({ ...form, category_id: e.target.value })}
              >
                {filteredCategories.map((category) => (
                  <MenuItem key={category.id} value={category.id.toString()}>
                    <Stack direction="row" alignItems="center" spacing={1}>
                      <Box
                        sx={{
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          backgroundColor: category.color,
                        }}
                      />
                      <span>{category.name}</span>
                    </Stack>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              label="Description"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              fullWidth
              multiline
              rows={2}
            />

            <TextField
              label="Date"
              type="date"
              value={form.transaction_date}
              onChange={(e) => setForm({ ...form, transaction_date: e.target.value })}
              fullWidth
              required
              slotProps={{ inputLabel: { shrink: true } }}
            />

            <TextField
              label="Merchant"
              value={form.merchant}
              onChange={(e) => setForm({ ...form, merchant: e.target.value })}
              fullWidth
            />

            <FormControl fullWidth>
              <InputLabel>Payment Method</InputLabel>
              <Select
                value={form.payment_method}
                label="Payment Method"
                onChange={(e) => setForm({ ...form, payment_method: e.target.value })}
              >
                <MenuItem value="card">Card</MenuItem>
                <MenuItem value="cash">Cash</MenuItem>
                <MenuItem value="bank_transfer">Bank Transfer</MenuItem>
                <MenuItem value="upi">UPI</MenuItem>
                <MenuItem value="other">Other</MenuItem>
              </Select>
            </FormControl>

            <FormControlLabel
              control={
                <Switch
                  checked={form.is_recurring}
                  onChange={(e) => setForm({ ...form, is_recurring: e.target.checked })}
                />
              }
              label="Recurring Transaction"
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button 
            variant="contained" 
            onClick={handleSubmit}
            disabled={!form.amount || !form.transaction_date}
          >
            {editingId ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Transaction</DialogTitle>
        <DialogContent>
          <Typography>Are you sure you want to delete this transaction? This action cannot be undone.</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" color="error" onClick={handleDelete}>
            Delete
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

export default Transactions;
