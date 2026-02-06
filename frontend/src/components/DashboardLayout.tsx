import { useState } from 'react';
import type { ReactNode } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Button,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Receipt as ReceiptIcon,
  Analytics as AnalyticsIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
  AutoAwesome as AIIcon,
  Warning as RiskIcon,
  AccountBalance as BudgetIcon,
} from '@mui/icons-material';
import { useDispatch } from 'react-redux';
import { logout } from '../store/slices/authSlice';

interface DashboardLayoutProps {
  children: ReactNode;
  title?: string;
}

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { text: 'Transactions', icon: <ReceiptIcon />, path: '/transactions' },
  { text: 'Analytics', icon: <AnalyticsIcon />, path: '/analytics' },
  { text: 'Risk & Predictions', icon: <RiskIcon />, path: '/risk-predictions' },
  { text: 'Budget Control', icon: <BudgetIcon />, path: '/budget-control' },
  { text: 'AI Insights', icon: <AIIcon />, path: '/ai-insights' },
  { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
];

function DashboardLayout({ children, title = 'AI Expense Risk Analyzer' }: DashboardLayoutProps) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <Box className="min-h-screen bg-gray-50">
      <AppBar position="sticky">
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={() => setDrawerOpen(true)}
            className="mr-4"
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            {title}
          </Typography>
          <Button color="inherit" onClick={handleLogout} startIcon={<LogoutIcon />}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Drawer anchor="left" open={drawerOpen} onClose={() => setDrawerOpen(false)}>
        <Box sx={{ width: 280 }} role="presentation">
          <List>
            <ListItem>
              <Typography variant="h6" sx={{ p: 2, fontWeight: 600 }}>
                Navigation
              </Typography>
            </ListItem>
            <Divider />
            {menuItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                <ListItemButton
                  onClick={() => {
                    navigate(item.path);
                    setDrawerOpen(false);
                  }}
                  selected={location.pathname === item.path}
                  sx={{
                    '&.Mui-selected': {
                      backgroundColor: 'primary.light',
                      color: 'primary.contrastText',
                      '& .MuiListItemIcon-root': {
                        color: 'primary.contrastText',
                      },
                    },
                  }}
                >
                  <ListItemIcon sx={{ color: location.pathname === item.path ? 'inherit' : 'text.secondary' }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      <Box component="main">
        {children}
      </Box>
    </Box>
  );
}

export default DashboardLayout;
