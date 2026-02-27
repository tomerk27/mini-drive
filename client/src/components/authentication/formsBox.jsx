import { Box, Link as MuiLink } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { EmailField, UsernameField, PasswordField, RememberMeField } from './inputFields';
import SubmitButton from './submitButton';

const FormsBox = ({ handleSubmit, emailRef, usernameRef, passwordRef, isLoading, mode }) => {
    const isSignup = mode === 'signup';

    const handleKeyDown = (event) => {
        if (event.key === 'Enter' && event.target.type !== 'submit') {
            event.preventDefault();
        }
    };

    return (
        <Box component="form" onSubmit={handleSubmit} onKeyDown={handleKeyDown} noValidate sx={{ width: '100%' }}>
            <EmailField emailRef={emailRef} isLoading={isLoading} />

            {isSignup && <UsernameField usernameRef={usernameRef} isLoading={isLoading} />}

            <PasswordField passwordRef={passwordRef} isLoading={isLoading} />

            <RememberMeField />

            <SubmitButton isLoading={isLoading} mode={mode} />

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <MuiLink
                    component={RouterLink}
                    to={isSignup ? "/login" : '/signup'}
                    variant="body2"
                    underline="hover"
                    sx={{ color: 'primary.main', fontWeight: 500, cursor: 'pointer' }}
                >
                    {isSignup ? "Have an account? Log in"
                        : "Don't have an account? Sign up"}
                </MuiLink>
            </Box>
        </Box>
    );
};

export default FormsBox;