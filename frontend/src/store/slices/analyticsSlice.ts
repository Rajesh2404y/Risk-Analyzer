import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

interface Summary {
  total_income: number;
  total_expenses: number;
  net_savings: number;
  transaction_count: number;
}

interface RiskScore {
  score: number;
  risk_level: string;
  factors: Record<string, unknown>;
}

interface AnalyticsState {
  summary: Summary | null;
  riskScore: RiskScore | null;
  loading: boolean;
  error: string | null;
}

const initialState: AnalyticsState = {
  summary: null,
  riskScore: null,
  loading: false,
  error: null,
};

const analyticsSlice = createSlice({
  name: 'analytics',
  initialState,
  reducers: {
    fetchSummaryStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchSummarySuccess: (state, action: PayloadAction<Summary>) => {
      state.loading = false;
      state.summary = action.payload;
      state.error = null;
    },
    fetchSummaryFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    setRiskScore: (state, action: PayloadAction<RiskScore>) => {
      state.riskScore = action.payload;
    },
  },
});

export const {
  fetchSummaryStart,
  fetchSummarySuccess,
  fetchSummaryFailure,
  setRiskScore,
} = analyticsSlice.actions;

export default analyticsSlice.reducer;
