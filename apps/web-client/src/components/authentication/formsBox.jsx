/**
 * formsBox.jsx
 *
 * Shared form wrapper used by both LoginPage and SignupPage.  The `mode`
 * prop ('login' | 'signup') controls which fields are shown and which
 * navigation link appears at the bottom.
 *
 * Enter-key handling is suppressed on non-submit elements to prevent
 * accidental submission while tabbing through fields.
 */
import { Box, Link as MuiLink } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { EmailField, UsernameField, PasswordField } from './inputFields';
import SubmitButton from './submitButton';

/**
 * Login/signup form container.
 *
 * @param {Function}          handleSubmit  - Form submit handler from useLogin or useSignup.
 * @param {React.RefObject}   emailRef      - Ref for the email input.
 * @param {React.RefObject}   [usernameRef] - Ref for the username input (signup only).
 * @param {React.RefObject}   passwordRef   - Ref for the password input.
 * @param {boolean}           isLoading     - Disables the submit button while the request is in flight.
 * @param {'login'|'signup'}  mode          - Controls which fields and navigation link appear.
 */
const FormsBox = ({ handleSubmit, emailRef, usernameRef, passwordRef, isLoading, mode }) => {
    const isSignup = mode === 'signup';

    // Prevent Enter from submitting before reaching the submit button naturally
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