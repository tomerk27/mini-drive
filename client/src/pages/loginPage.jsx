import {
  Box,
  Typography,
  Container,
  Alert,
  Paper
} from '@mui/material';
import useLogin from '../hooks/auth/useLogin';
import FormsBox from '../components/authentication/formsBox';

const LoginPage = () => {
  const { handleSubmit, isLoading, error, emailRef, passwordRef } = useLogin();

  return (
    <Container component="login-container" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography component="h1" variant="h5" align="center" gutterBottom>
            Sign in to Drive
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <FormsBox
            handleSubmit={handleSubmit}
            emailRef={emailRef}
            passwordRef={passwordRef}
            isLoading={isLoading}
          />

        </Paper>
      </Box>
    </Container>
  );
};

export default LoginPage;