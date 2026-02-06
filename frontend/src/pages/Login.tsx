import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import {
  Container,
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  Stack,
} from '@mui/material';
import { loginStart, loginSuccess, loginFailure } from '../store/slices/authSlice';
import { authAPI } from '../services/api';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    dispatch(loginStart());

    try {
      const response = await authAPI.login(email, password);
      dispatch(loginSuccess({
        user: response.data.user,
        token: response.data.access_token,
      }));
      navigate('/dashboard');
    } catch (err: unknown) {
      const message = (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Login failed';
      setError(message);
      dispatch(loginFailure(message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box className="min-h-screen flex items-center justify-center" sx={{ bgcolor: 'background.default' }}>
      <Container maxWidth="sm">
        <Card elevation={3}>
          <CardContent className="p-8">
            <Stack spacing={3}>
              <Box className="text-center">
                <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600, color: 'primary.main' }}>
                  Expense Risk Analyzer
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Login to manage your finances with AI
                </Typography>
              </Box>

              {error && <Alert severity="error">{error}</Alert>}

              <form onSubmit={handleSubmit}>
                <Stack spacing={2}>
                  <TextField
                    label="Email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    fullWidth
                  />
                  <TextField
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    fullWidth
                  />
                  <Button
                    type="submit"
                    variant="contained"
                    size="large"
                    fullWidth
                    disabled={loading}
                  >
                    {loading ? 'Logging in...' : 'Login'}
                  </Button>
                </Stack>
              </form>

              <Box className="text-center">
                <Typography variant="body2">
                  Don't have an account?{' '}
                  <Link to="/register" style={{ color: 'var(--mui-palette-primary-main)' }}>
                    Register here
                  </Link>
                </Typography>
              </Box>
            </Stack>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

export default Login;
