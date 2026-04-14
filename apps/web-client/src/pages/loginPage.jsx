import {
  Box,
  Typography,
  Container,
  Paper,
  Alert
} from '@mui/material';
import FormsBox from '../components/authentication/formsBox';
import useLogin from '../hooks/auth/useLogin';


const LoginPage = () => {
  const { handleSubmit, isLoading, error, emailRef, passwordRef } = useLogin();

  return (
    <Container component="login-container" maxWidth="xs">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          bgcolor: 'background.default',
          p: 2
        }}
      >
        <Paper
          elevation={0}
          sx={{
            minHeight: '600px',
            justifyContent: 'center',
            p: 6,
            gap: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
            maxWidth: '500px',
            border: '1px solid #e0e0e0',
            borderRadius: 4,
            bgcolor: 'background.paper'
          }}
        >

          <Typography component="h1" variant="h5" sx={{ mb: 1, color: 'text.primary' }}>
            Log in
          </Typography>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Welcome user, please log in to continue
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2, width: '100%' }} variant="standard">
              {error}
            </Alert>
          )}

          <FormsBox
            handleSubmit={handleSubmit}
            emailRef={emailRef}
            passwordRef={passwordRef}
            isLoading={isLoading}
            mode='login'
          />
        </Paper>
      </Box>
    </Container>
  );
};

export default LoginPage;