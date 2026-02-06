import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

interface Transaction {
  id: number;
  type: string;
  amount: number;
  category: {
    id: number;
    name: string;
    color: string;
    icon: string;
  } | null;
  description: string;
  transaction_date: string;
  merchant: string;
  payment_method: string;
  is_recurring: boolean;
}

interface TransactionsState {
  transactions: Transaction[];
  loading: boolean;
  error: string | null;
}

const initialState: TransactionsState = {
  transactions: [],
  loading: false,
  error: null,
};

const transactionsSlice = createSlice({
  name: 'transactions',
  initialState,
  reducers: {
    fetchTransactionsStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchTransactionsSuccess: (state, action: PayloadAction<Transaction[]>) => {
      state.loading = false;
      state.transactions = action.payload;
      state.error = null;
    },
    fetchTransactionsFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    addTransaction: (state, action: PayloadAction<Transaction>) => {
      state.transactions.unshift(action.payload);
    },
    updateTransaction: (state, action: PayloadAction<Transaction>) => {
      const index = state.transactions.findIndex(t => t.id === action.payload.id);
      if (index !== -1) {
        state.transactions[index] = action.payload;
      }
    },
    deleteTransaction: (state, action: PayloadAction<number>) => {
      state.transactions = state.transactions.filter(t => t.id !== action.payload);
    },
  },
});

export const {
  fetchTransactionsStart,
  fetchTransactionsSuccess,
  fetchTransactionsFailure,
  addTransaction,
  updateTransaction,
  deleteTransaction,
} = transactionsSlice.actions;

export default transactionsSlice.reducer;
