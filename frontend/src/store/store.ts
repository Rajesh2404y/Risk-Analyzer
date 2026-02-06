import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import transactionsReducer from './slices/transactionsSlice';
import analyticsReducer from './slices/analyticsSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    transactions: transactionsReducer,
    analytics: analyticsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
