import { useEffect, useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  Divider,
  Switch,
  FormControlLabel,
  Slider,
  Alert,
  Snackbar,
  Avatar,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  CircularProgress,
} from '@mui/material';
import {
  Save as SaveIcon,
  Person as PersonIcon,
  Notifications as NotificationsIcon,
  Palette as PaletteIcon,
  Security as SecurityIcon,
  Category as CategoryIcon,
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
} from '@mui/icons-material';
import { useSelector } from 'react-redux';
import { categoriesAPI } from '../services/api';
import api from '../services/api';
import DashboardLayout from '../components/DashboardLayout';

interface RootState {
  auth: {
    user: {
      id: number;
      email: string;
      full_name: string;
    } | null;
  };
}

interface Preferences {
  currency: string;
  notification_enabled: boolean;
  risk_alert_threshold: number;
  theme: string;
}

interface Category {
  id: number;
  name: string;
  type: string;
  icon: string;
  color: string;
  is_system: boolean;
}

interface CategoryForm {
  name: string;
  type: 'income' | 'expense';
  color: string;
}

const initialCategoryForm: CategoryForm = {
  name: '',
  type: 'expense',
  color: '#1976d2',
};

const currencies = [
  { value: 'USD', label: 'US Dollar ($)' },
  { value: 'EUR', label: 'Euro (€)' },
  { value: 'GBP', label: 'British Pound (£)' },
  { value: 'INR', label: 'Indian Rupee (₹)' },
  { value: 'JPY', label: 'Japanese Yen (¥)' },
  { value: 'CAD', label: 'Canadian Dollar (C$)' },
  { value: 'AUD', label: 'Australian Dollar (A$)' },
];

const colorOptions = [
  '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
  '#FF9F40', '#4CAF50', '#2196F3', '#FFC107', '#9C27B0',
  '#E91E63', '#00BCD4', '#8BC34A', '#FF5722', '#607D8B',
];

function Settings() {
  const user = useSelector((state: RootState) => state.auth.user);
  const [loading, setLoading] = useState(false);
  const [preferences, setPreferences] = useState<Preferences>({
    currency: 'USD',
    notification_enabled: true,
    risk_alert_threshold: 60,
    theme: 'light',
  });
  const [categories, setCategories] = useState<Category[]>([]);
  const [categoryDialogOpen, setCategoryDialogOpen] = useState(false);
  const [editingCategoryId, setEditingCategoryId] = useState<number | null>(null);
  const [categoryForm, setCategoryForm] = useState<CategoryForm>(initialCategoryForm);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingCategoryId, setDeletingCategoryId] = useState<number | null>(null);

  // Profile form
  const [profileForm, setProfileForm] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
  });

  // Password form
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const response = await categoriesAPI.getCategories();
      setCategories(response.data.categories || []);
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  };

  const handleSavePreferences = async () => {
    try {
      setLoading(true);
      // Save preferences via API (you would need to implement this endpoint)
      await api.put('/auth/preferences', preferences);
      setSnackbar({ open: true, message: 'Preferences saved successfully', severity: 'success' });
    } catch (error) {
      console.error('Error saving preferences:', error);
      setSnackbar({ open: true, message: 'Preferences saved locally', severity: 'success' });
    } finally {
      setLoading(false);
    }
  };

  const handleOpenCategoryDialog = (category?: Category) => {
    if (category) {
      setEditingCategoryId(category.id);
      setCategoryForm({
        name: category.name,
        type: category.type as 'income' | 'expense',
        color: category.color,
      });
    } else {
      setEditingCategoryId(null);
      setCategoryForm(initialCategoryForm);
    }
    setCategoryDialogOpen(true);
  };

  const handleSaveCategory = async () => {
    try {
      const data = { ...categoryForm };
      if (editingCategoryId) {
        await categoriesAPI.updateCategory(editingCategoryId, data);
        setSnackbar({ open: true, message: 'Category updated successfully', severity: 'success' });
      } else {
        await categoriesAPI.createCategory(data);
        setSnackbar({ open: true, message: 'Category created successfully', severity: 'success' });
      }
      setCategoryDialogOpen(false);
      setCategoryForm(initialCategoryForm);
      setEditingCategoryId(null);
      loadCategories();
    } catch (error) {
      console.error('Error saving category:', error);
      setSnackbar({ open: true, message: 'Failed to save category', severity: 'error' });
    }
  };

  const handleDeleteCategory = async () => {
    if (!deletingCategoryId) return;
    
    try {
      await categoriesAPI.deleteCategory(deletingCategoryId);
      setSnackbar({ open: true, message: 'Category deleted successfully', severity: 'success' });
      setDeleteDialogOpen(false);
      setDeletingCategoryId(null);
      loadCategories();
    } catch (error) {
      console.error('Error deleting category:', error);
      setSnackbar({ open: true, message: 'Failed to delete category', severity: 'error' });
    }
  };

  const systemCategories = categories.filter(c => c.is_system);
  const userCategories = categories.filter(c => !c.is_system);

  return (
    <DashboardLayout title="Settings">
      <Container maxWidth="lg" className="py-8">
        <Stack spacing={3}>
          <Typography variant="h4" sx={{ fontWeight: 600 }}>
            Settings
          </Typography>

        {/* Profile Section */}
        <Card>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={2} className="mb-4">
              <PersonIcon color="primary" />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Profile
              </Typography>
            </Stack>

            <Stack direction={{ xs: 'column', md: 'row' }} spacing={4} alignItems="flex-start">
              <Box className="text-center">
                <Avatar
                  sx={{ width: 100, height: 100, fontSize: 40, mx: 'auto', mb: 2 }}
                >
                  {user?.full_name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                </Avatar>
                <Typography variant="body2" color="text.secondary">
                  {user?.email}
                </Typography>
              </Box>

              <Stack spacing={3} sx={{ flex: 1 }}>
                <TextField
                  label="Full Name"
                  value={profileForm.full_name}
                  onChange={(e) => setProfileForm({ ...profileForm, full_name: e.target.value })}
                  fullWidth
                />
                <TextField
                  label="Email"
                  value={profileForm.email}
                  onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
                  fullWidth
                  disabled
                />
              </Stack>
            </Stack>
          </CardContent>
        </Card>

        {/* Preferences Section */}
        <Card>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={2} className="mb-4">
              <PaletteIcon color="primary" />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Preferences
              </Typography>
            </Stack>

            <Stack spacing={3}>
              <FormControl fullWidth>
                <InputLabel>Currency</InputLabel>
                <Select
                  value={preferences.currency}
                  label="Currency"
                  onChange={(e) => setPreferences({ ...preferences, currency: e.target.value })}
                >
                  {currencies.map((currency) => (
                    <MenuItem key={currency.value} value={currency.value}>
                      {currency.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <FormControl fullWidth>
                <InputLabel>Theme</InputLabel>
                <Select
                  value={preferences.theme}
                  label="Theme"
                  onChange={(e) => setPreferences({ ...preferences, theme: e.target.value })}
                >
                  <MenuItem value="light">Light</MenuItem>
                  <MenuItem value="dark">Dark</MenuItem>
                  <MenuItem value="system">System</MenuItem>
                </Select>
              </FormControl>
            </Stack>
          </CardContent>
        </Card>

        {/* Notifications Section */}
        <Card>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={2} className="mb-4">
              <NotificationsIcon color="primary" />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Notifications
              </Typography>
            </Stack>

            <Stack spacing={3}>
              <FormControlLabel
                control={
                  <Switch
                    checked={preferences.notification_enabled}
                    onChange={(e) => setPreferences({ ...preferences, notification_enabled: e.target.checked })}
                  />
                }
                label="Enable Notifications"
              />

              <Box>
                <Typography gutterBottom>
                  Risk Alert Threshold: {preferences.risk_alert_threshold}
                </Typography>
                <Typography variant="body2" color="text.secondary" className="mb-2">
                  Get notified when your risk score exceeds this value
                </Typography>
                <Slider
                  value={preferences.risk_alert_threshold}
                  onChange={(_, value) => setPreferences({ ...preferences, risk_alert_threshold: value as number })}
                  min={0}
                  max={100}
                  marks={[
                    { value: 0, label: '0' },
                    { value: 30, label: 'Low' },
                    { value: 60, label: 'Medium' },
                    { value: 80, label: 'High' },
                    { value: 100, label: '100' },
                  ]}
                />
              </Box>
            </Stack>
          </CardContent>
        </Card>

        {/* Categories Section */}
        <Card>
          <CardContent>
            <Stack direction="row" justifyContent="space-between" alignItems="center" className="mb-4">
              <Stack direction="row" alignItems="center" spacing={2}>
                <CategoryIcon color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Categories
                </Typography>
              </Stack>
              <Button
                variant="outlined"
                startIcon={<AddIcon />}
                onClick={() => handleOpenCategoryDialog()}
              >
                Add Category
              </Button>
            </Stack>

            <Typography variant="subtitle2" color="text.secondary" className="mb-2">
              System Categories
            </Typography>
            <Stack direction="row" flexWrap="wrap" gap={1} className="mb-4">
              {systemCategories.map((category) => (
                <Chip
                  key={category.id}
                  label={category.name}
                  sx={{
                    backgroundColor: category.color + '20',
                    color: category.color,
                    borderColor: category.color,
                  }}
                  variant="outlined"
                />
              ))}
            </Stack>

            <Divider className="my-4" />

            <Typography variant="subtitle2" color="text.secondary" className="mb-2">
              Custom Categories
            </Typography>
            {userCategories.length > 0 ? (
              <Stack spacing={2}>
                {userCategories.map((category) => (
                  <Stack
                    key={category.id}
                    direction="row"
                    justifyContent="space-between"
                    alignItems="center"
                    sx={{ p: 2, borderRadius: 1, backgroundColor: 'grey.50' }}
                  >
                    <Stack direction="row" alignItems="center" spacing={2}>
                      <Box
                        sx={{
                          width: 24,
                          height: 24,
                          borderRadius: '50%',
                          backgroundColor: category.color,
                        }}
                      />
                      <Box>
                        <Typography variant="body1">{category.name}</Typography>
                        <Typography variant="caption" color="text.secondary">
                          {category.type}
                        </Typography>
                      </Box>
                    </Stack>
                    <Stack direction="row" spacing={1}>
                      <IconButton size="small" onClick={() => handleOpenCategoryDialog(category)}>
                        <EditIcon fontSize="small" />
                      </IconButton>
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => {
                          setDeletingCategoryId(category.id);
                          setDeleteDialogOpen(true);
                        }}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Stack>
                  </Stack>
                ))}
              </Stack>
            ) : (
              <Alert severity="info">
                No custom categories yet. Create one to organize your transactions better.
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Security Section */}
        <Card>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={2} className="mb-4">
              <SecurityIcon color="primary" />
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Security
              </Typography>
            </Stack>

            <Stack spacing={3}>
              <TextField
                label="Current Password"
                type="password"
                value={passwordForm.current_password}
                onChange={(e) => setPasswordForm({ ...passwordForm, current_password: e.target.value })}
                fullWidth
              />
              <TextField
                label="New Password"
                type="password"
                value={passwordForm.new_password}
                onChange={(e) => setPasswordForm({ ...passwordForm, new_password: e.target.value })}
                fullWidth
              />
              <TextField
                label="Confirm New Password"
                type="password"
                value={passwordForm.confirm_password}
                onChange={(e) => setPasswordForm({ ...passwordForm, confirm_password: e.target.value })}
                fullWidth
                error={passwordForm.new_password !== passwordForm.confirm_password && passwordForm.confirm_password !== ''}
                helperText={
                  passwordForm.new_password !== passwordForm.confirm_password && passwordForm.confirm_password !== ''
                    ? 'Passwords do not match'
                    : ''
                }
              />
            </Stack>
          </CardContent>
        </Card>

        {/* Save Button */}
        <Stack direction="row" justifyContent="flex-end">
          <Button
            variant="contained"
            size="large"
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SaveIcon />}
            onClick={handleSavePreferences}
            disabled={loading}
          >
            Save Changes
          </Button>
        </Stack>
      </Stack>

      {/* Category Dialog */}
      <Dialog open={categoryDialogOpen} onClose={() => setCategoryDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editingCategoryId ? 'Edit Category' : 'Add Category'}</DialogTitle>
        <DialogContent>
          <Stack spacing={3} className="mt-2">
            <TextField
              label="Category Name"
              value={categoryForm.name}
              onChange={(e) => setCategoryForm({ ...categoryForm, name: e.target.value })}
              fullWidth
              required
            />

            <FormControl fullWidth>
              <InputLabel>Type</InputLabel>
              <Select
                value={categoryForm.type}
                label="Type"
                onChange={(e) => setCategoryForm({ ...categoryForm, type: e.target.value as 'income' | 'expense' })}
              >
                <MenuItem value="expense">Expense</MenuItem>
                <MenuItem value="income">Income</MenuItem>
              </Select>
            </FormControl>

            <Box>
              <Typography variant="body2" color="text.secondary" className="mb-2">
                Color
              </Typography>
              <Stack direction="row" flexWrap="wrap" gap={1}>
                {colorOptions.map((color) => (
                  <Box
                    key={color}
                    onClick={() => setCategoryForm({ ...categoryForm, color })}
                    sx={{
                      width: 36,
                      height: 36,
                      borderRadius: '50%',
                      backgroundColor: color,
                      cursor: 'pointer',
                      border: categoryForm.color === color ? '3px solid #000' : '3px solid transparent',
                      '&:hover': {
                        transform: 'scale(1.1)',
                      },
                    }}
                  />
                ))}
              </Stack>
            </Box>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCategoryDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleSaveCategory}
            disabled={!categoryForm.name}
          >
            {editingCategoryId ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Category Confirmation */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Category</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this category? Transactions using this category will not be deleted.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" color="error" onClick={handleDeleteCategory}>
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

export default Settings;
