import { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  CardHeader,
  Stack,
  Chip,
  CircularProgress,
  Alert,
  IconButton,
  Collapse,
  Divider,
  Button,
  Paper,
} from '@mui/material';
import {
  TrendingUp,
  Warning,
  Assessment,
  CalendarMonth,
  Summarize,
  DataUsage,
  Lightbulb,
  ExpandMore,
  ExpandLess,
  Refresh,
  AutoAwesome,
  Email,
} from '@mui/icons-material';
import api from '../services/api';
import DashboardLayout from '../components/DashboardLayout';

interface InsightData {
  type: string;
  title: string;
  description: string;
  insight: string;
  generated_at?: string;
  error?: string;
}

interface InsightCardProps {
  type: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  color: string;
}

const insightConfigs: InsightCardProps[] = [
  {
    type: 'executive-summary',
    title: 'Executive Summary',
    description: 'Management-level overview and key recommendations',
    icon: <Summarize />,
    color: '#1976d2',
  },
  {
    type: 'transaction-analysis',
    title: 'Transaction Analysis',
    description: 'Key trends, patterns, and performance insights',
    icon: <TrendingUp />,
    color: '#2e7d32',
  },
  {
    type: 'anomaly-detection',
    title: 'Anomaly Detection',
    description: 'Unusual patterns and their explanations',
    icon: <Warning />,
    color: '#ed6c02',
  },
  {
    type: 'forecast-comparison',
    title: 'Forecast vs Actual',
    description: 'Compare predictions with actual performance',
    icon: <Assessment />,
    color: '#9c27b0',
  },
  {
    type: 'seasonality',
    title: 'Seasonality Patterns',
    description: 'Recurring trends and seasonal impacts',
    icon: <CalendarMonth />,
    color: '#0288d1',
  },
  {
    type: 'data-quality',
    title: 'Data Quality Assessment',
    description: 'Reliability and accuracy evaluation',
    icon: <DataUsage />,
    color: '#757575',
  },
  {
    type: 'recommendations',
    title: 'Action Recommendations',
    description: 'Actionable steps to improve performance',
    icon: <Lightbulb />,
    color: '#ffc107',
  },
];

function InsightCard({ config }: { config: InsightCardProps }) {
  const [data, setData] = useState<InsightData | null>(null);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchInsight = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get(`/ai-insights/${config.type}`);
      setData(response.data);
      setExpanded(true);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch insight';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const formatInsight = (text: string) => {
    // Split by newlines and render paragraphs
    return text.split('\n').map((paragraph, index) => {
      if (paragraph.trim().startsWith('•') || paragraph.trim().startsWith('-')) {
        return (
          <Typography
            key={index}
            variant="body2"
            className="pl-4 py-1"
            sx={{ color: 'text.secondary' }}
          >
            {paragraph}
          </Typography>
        );
      }
      if (paragraph.trim().startsWith('**') || paragraph.trim().startsWith('##')) {
        return (
          <Typography
            key={index}
            variant="subtitle2"
            className="pt-3 pb-1"
            sx={{ fontWeight: 600 }}
          >
            {paragraph.replace(/\*\*/g, '').replace(/##/g, '')}
          </Typography>
        );
      }
      if (paragraph.trim()) {
        return (
          <Typography
            key={index}
            variant="body2"
            className="py-1"
            sx={{ color: 'text.primary' }}
          >
            {paragraph}
          </Typography>
        );
      }
      return null;
    });
  };

  return (
    <Card
      elevation={2}
      sx={{
        borderLeft: `4px solid ${config.color}`,
        transition: 'all 0.3s ease',
        '&:hover': {
          boxShadow: 4,
        },
      }}
    >
      <CardHeader
        avatar={
          <Box
            sx={{
              backgroundColor: `${config.color}15`,
              borderRadius: '12px',
              p: 1,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: config.color,
            }}
          >
            {config.icon}
          </Box>
        }
        action={
          <Stack direction="row" spacing={1} alignItems="center">
            {data && (
              <Chip
                size="small"
                label="Generated"
                color="success"
                variant="outlined"
              />
            )}
            <IconButton
              onClick={fetchInsight}
              disabled={loading}
              size="small"
              sx={{ color: config.color }}
            >
              {loading ? <CircularProgress size={20} /> : <Refresh />}
            </IconButton>
            {data && (
              <IconButton
                onClick={() => setExpanded(!expanded)}
                size="small"
              >
                {expanded ? <ExpandLess /> : <ExpandMore />}
              </IconButton>
            )}
          </Stack>
        }
        title={
          <Typography variant="h6" sx={{ fontWeight: 500 }}>
            {config.title}
          </Typography>
        }
        subheader={
          <Typography variant="body2" color="text.secondary">
            {config.description}
          </Typography>
        }
      />
      
      {!data && !loading && !error && (
        <CardContent>
          <Button
            variant="outlined"
            startIcon={<AutoAwesome />}
            onClick={fetchInsight}
            sx={{ borderColor: config.color, color: config.color }}
          >
            Generate AI Insight
          </Button>
        </CardContent>
      )}

      {error && (
        <CardContent>
          <Alert severity="error" onClose={() => setError(null)}>
            {error}
          </Alert>
        </CardContent>
      )}

      <Collapse in={expanded && !!data}>
        <Divider />
        <CardContent>
          {data?.insight && (
            <Paper
              elevation={0}
              sx={{
                p: 2,
                backgroundColor: 'grey.50',
                borderRadius: 2,
                maxHeight: 400,
                overflow: 'auto',
              }}
            >
              {formatInsight(data.insight)}
            </Paper>
          )}
          {data?.generated_at && (
            <Typography
              variant="caption"
              color="text.secondary"
              className="mt-2 block"
            >
              Generated: {new Date(data.generated_at).toLocaleString()}
            </Typography>
          )}
        </CardContent>
      </Collapse>
    </Card>
  );
}

function AIInsights() {
  const [emailLoading, setEmailLoading] = useState(false);
  const [emailStatus, setEmailStatus] = useState<{ type: 'success' | 'error', message: string } | null>(null);

  const sendEmailAlert = async () => {
    setEmailLoading(true);
    setEmailStatus(null);
    try {
      const response = await api.post('/recommendations/send-alerts');
      setEmailStatus({ 
        type: 'success', 
        message: response.data.message || 'Email alert sent successfully!' 
      });
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send email';
      setEmailStatus({ type: 'error', message: errorMessage });
    } finally {
      setEmailLoading(false);
    }
  };

  return (
    <DashboardLayout title="AI Insights">
      <Container maxWidth="lg" className="py-8">
        <Box className="mb-8">
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          className="mb-2"
        >
          <Stack direction="row" alignItems="center" spacing={2}>
            <Box
              sx={{
                backgroundColor: 'primary.main',
                borderRadius: '12px',
                p: 1.5,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <AutoAwesome sx={{ color: 'white', fontSize: 28 }} />
            </Box>
            <Box>
              <Typography variant="h4" sx={{ fontWeight: 600 }}>
                AI-Powered Insights
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Intelligent analysis of your financial data using GPT-4
              </Typography>
            </Box>
          </Stack>
          <Button
            variant="contained"
            startIcon={emailLoading ? <CircularProgress size={20} color="inherit" /> : <Email />}
            onClick={sendEmailAlert}
            disabled={emailLoading}
            sx={{ minWidth: 180 }}
          >
            {emailLoading ? 'Sending...' : 'Send Email Alert'}
          </Button>
        </Stack>
      </Box>

      {emailStatus && (
        <Alert 
          severity={emailStatus.type} 
          onClose={() => setEmailStatus(null)}
          className="mb-4"
        >
          {emailStatus.message}
        </Alert>
      )}

      <Alert severity="info" className="mb-6" icon={<AutoAwesome />}>
        Click on any card below to generate AI-powered insights based on your transaction data.
        Each analysis is generated fresh using OpenAI's GPT-4 model.
      </Alert>

      <Stack spacing={3}>
        {insightConfigs.map((config) => (
          <InsightCard key={config.type} config={config} />
        ))}
      </Stack>
      </Container>
    </DashboardLayout>
  );
}

export default AIInsights;
