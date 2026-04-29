/**
 * submitButton.jsx
 *
 * Full-width submit button shared by login and signup forms.  Shows a spinner
 * while the request is in flight and disables itself to prevent double-submission.
 */
import { Button, CircularProgress } from '@mui/material';

/**
 * Submit button for auth forms.
 *
 * @param {boolean}           isLoading - Replaces button text with a spinner when true.
 * @param {'login'|'signup'}  mode      - Determines the button label.
 */
const SubmitButton = ({ isLoading, mode }) => {
    const isSignup = mode === "signup";
    return (
        <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={isLoading}
            sx={{ mt: 3, mb: 2, py: 1 }}
        >
            {isLoading ? <CircularProgress size={24} color="inherit" /> : isSignup ? 'Sign up' : 'Log in'}
        </Button>
    );
};

export default SubmitButton;