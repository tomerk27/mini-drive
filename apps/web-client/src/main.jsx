/**
 * main.jsx
 *
 * Application entry point. Mounts the React app into the #root DOM element and
 * wraps it with:
 *   - AuthProvider   — supplies JWT-based auth state to all components
 *   - ThemeProvider  — applies the custom MUI theme (indigo palette, soft corners)
 *   - CssBaseline    — normalises browser default styles
 *
 * The MUI theme defined here is the single source of truth for colors,
 * typography, border radii, and component overrides across the whole client.
 */
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App.jsx';
import { AuthProvider } from './context/auth/authProvider.jsx';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#6366f1', // Indigo 500 - more modern than Google Blue
      light: '#818cf8',
      dark: '#4f46e5',
    },
    secondary: {
      main: '#ec4899', // Pink 500 for accents
    },
    background: {
      default: '#f9fafb', // Very light gray/slate
      paper: '#ffffff',
    },
    text: {
      primary: '#111827', // Gray 900
      secondary: '#4b5563', // Gray 600
    },
  },
  shape: {
    borderRadius: 16, // Softer corners
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h5: {
      fontWeight: 700,
      letterSpacing: '-0.025em',
    },
    h6: {
      fontWeight: 600,
      letterSpacing: '-0.025em',
    },
    button: {
      fontWeight: 600,
      textTransform: 'none',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          padding: '8px 16px',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
          },
        },
        containedPrimary: {
          '&:hover': {
            backgroundColor: '#4f46e5',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff',
          '& fieldset': {
            borderColor: '#e5e7eb',
          },
          '&:hover fieldset': {
            borderColor: '#d1d5db',
          },
          '&.Mui-focused fieldset': {
            borderColor: '#6366f1',
          },
        },
      },
    },
  },
});


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </AuthProvider>
  </StrictMode>,
);