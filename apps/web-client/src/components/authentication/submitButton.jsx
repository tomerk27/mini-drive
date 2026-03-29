import { Button, CircularProgress } from '@mui/material';

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