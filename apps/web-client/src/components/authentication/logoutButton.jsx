/**
 * logoutButton.jsx
 *
 * A self-contained logout button placed at the bottom of the sidebar.
 * Manages its own loading and error state via the useLogout hook and
 * shows an error Alert inline below the button if the logout fails.
 */
import { Button, CircularProgress, Alert, Box } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import useLogout from '../../hooks/auth/useLogout';

const LogoutButton = () => {
    const { handleLogOut, isLoading, error } = useLogout();

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <Button
                variant="text"
                color="error"
                fullWidth
                onClick={handleLogOut}
                disabled={isLoading}
                startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <LogoutIcon />}
                sx={{
                    borderRadius: 3,
                    textTransform: 'none',
                    fontWeight: 500,
                    justifyContent: 'flex-start',
                    px: 2,
                    py: 1,
                    '&:hover': { bgcolor: 'error.50' },
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