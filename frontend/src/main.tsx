import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux'
import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { CacheProvider } from '@emotion/react'
import createCache from '@emotion/cache'
import { store } from './store/store'
import theme from './theme'
import App from './App'
import './index.css'

const createEmotionCache = () => {
  return createCache({
    key: 'mui',
    prepend: true,
  });
};

const emotionCache = createEmotionCache();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider store={store}>
      <CacheProvider value={emotionCache}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <App />
        </ThemeProvider>
      </CacheProvider>
    </Provider>
  </StrictMode>,
)
