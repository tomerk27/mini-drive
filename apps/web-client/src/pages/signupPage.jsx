/**
 * signupPage.jsx
 *
 * Public page rendered at /signup.  Mirrors loginPage but uses the signup
 * form variant (adds the username field).  All form logic is handled by
 * the useSignup hook.
 */
import {
  Box,
  Typography,
  Container,
  Paper,
  Alert
} from '@mui/material';
import FormsBox from '../components/authentication/formsBox';
import CyberDriveMark from '../components/topBar/CyberDriveMark';
import useSignup from '../hooks/auth/useSignup';

const SignupPage = () => {
  const { handleSubmit, isLoading, error, emailRef, usernameRef, passwordRef } = useSignup();

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

          <Box sx={{ mb: 1, filter: 'drop-shadow(0 8px 14px rgb(99 102 241 / 0.45))' }}>
            <CyberDriveMark size={56} />
          </Box>

          <Typography component="h1" variant="h5" sx={{ mb: 1, color: 'text.primary' }}>
            Sign up
          </Typography>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Welcome user, please sign up to continue
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2, width: '100%' }} variant="standard">
              {error}
            </Alert>
          )}

          <FormsBox
            handleSubmit={handleSubmit}
            emailRef={emailRef}
            usernameRef={usernameRef}
            passwordRef={passwordRef}
            isLoading={isLoading}
            mode='signup'
          />
        </Paper>
      </Box>
    </Container>
  );
};

export default SignupPage;