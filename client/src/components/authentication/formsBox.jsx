import { Box, Link as MuiLink } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { EmailField, PasswordField, RememberMeField } from './inputFields';
import SubmitButton from './submitButton';

const FormsBox = ({ handleSubmit, emailRef, passwordRef, isLoading }) => {
    return (
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ width: '100%' }}>
            <EmailField emailRef={emailRef} isLoading={isLoading} />

            <PasswordField passwordRef={passwordRef} isLoading={isLoading} />

            <RememberMeField />

            <SubmitButton isLoading={isLoading} handleSubmit={handleSubmit} />

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <MuiLink 
                    component={RouterLink}
                    to="/dashboard" 
                    variant="body2" 
                    underline="hover" 
                    sx={{ color: 'primary.main', fontWeight: 500, cursor: 'pointer' }}
                >
                    Don't have an account? Sign up
                </MuiLink>
            </Box>
        </Box>
    );
};

export default FormsBox;