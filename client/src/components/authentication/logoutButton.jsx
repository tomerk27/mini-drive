import { Button, CircularProgress, Alert, Box } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import useLogout from '../../hooks/auth/useLogout';

const LogoutButton = () => {
    const { handleLogOut, isLoading, error } = useLogout();

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <Button
                variant="outlined"
                color="error"
                onClick={handleLogOut}
                disabled={isLoading}
                startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <LogoutIcon />}
                sx={{
                    borderRadius: 20,
                    textTransform: 'none',
                    fontWeight: 'bold',
                }}
            >
                {isLoading ? 'Logging out...' : 'Log out'}
            </Button>

            {error && (
                <Alert severity="error" sx={{ mt: 1 }}>
                    Logout failed: {typeof error === 'string' ? error : error.message}
                </Alert>
            )}
        </Box>
    );
};

export default LogoutButton;