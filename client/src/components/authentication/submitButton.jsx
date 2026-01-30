import { Button } from '@mui/material';

const SubmitButton = ({ isLoading, handleSubmit }) => {
    return (
        <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            onClick={handleSubmit}
            disabled={isLoading}
        >
            {isLoading ? 'Signing in...' : 'Sign In'}
        </Button>
    );
};

export default SubmitButton;