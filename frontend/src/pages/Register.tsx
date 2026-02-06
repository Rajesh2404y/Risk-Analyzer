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
import { loginSuccess } from '../store/slices/authSlice';
import { authAPI } from '../services/api';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.register(email, password, fullName);
      dispatch(loginSuccess({
        user: response.data.user,
        token: response.data.access_token,
      }));
      navigate('/dashboard');
    } catch (err: unknown) {
      const message = (err as { response?: { data?: { error?: string } } })?.response?.data?.error || 'Registration failed';
      setError(message);
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
                  Create Account
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Start tracking your expenses with AI-powered insights
                </Typography>
              </Box>

              {error && <Alert severity="error">{error}</Alert>}

              <form onSubmit={handleSubmit}>
                <Stack spacing={2}>
                  <TextField
                    label="Full Name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    required
                    fullWidth
                  />
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
                    helperText="Minimum 8 characters"
                  />
                  <Button
                    type="submit"
                    variant="contained"
                    size="large"
                    fullWidth
                    disabled={loading}
                  >
                    {loading ? 'Creating Account...' : 'Register'}
                  </Button>
                </Stack>
              </form>

              <Box className="text-center">
                <Typography variant="body2">
                  Already have an account?{' '}
                  <Link to="/login" style={{ color: 'var(--mui-palette-primary-main)' }}>
                    Login here
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

export default Register;
