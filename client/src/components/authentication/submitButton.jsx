import { Button, CircularProgress } from '@mui/material';

const SubmitButton = ({ isLoading, handleSubmit }) => {
    return (
        <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={isLoading}
            sx={{ mt: 3, mb: 2, py: 1 }}
            onClick={handleSubmit}
        >
            {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Sign In'}
        </Button>
    );
};

export default SubmitButton;