import { Button } from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';

const GoogleConnectionButton = () => {
    return (
        <Button
            fullWidth
            variant="outlined"
            startIcon={<GoogleIcon />}
            sx={{
                mb: 3,
                color: 'text.primary',
                borderColor: '#e0e0e0',
                backgroundColor: '#fff',
                textTransform: 'none',
                '&:hover': {
                    borderColor: '#bdbdbd',
                    backgroundColor: '#f5f5f5'
                }
            }}
            onClick={() => alert("Google login implementation required")}
        >
            Sign in with Google
        </Button>
    )
}

export default GoogleConnectionButton