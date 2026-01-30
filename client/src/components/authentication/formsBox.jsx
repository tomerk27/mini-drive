import { Box } from '@mui/material';
import { Link } from 'react-router-dom';
import { EmailField, PasswordField } from './inputFields';
import SubmitButton from './submitButton';

const FormsBox = ({ handleSubmit, emailRef, passwordRef, isLoading }) => {
    return (
        <Box component="form" noValidate>
            <EmailField emailRef={emailRef} isLoading={isLoading} />

            <PasswordField passwordRef={passwordRef} isLoading={isLoading} />

            <SubmitButton isLoading={isLoading} handleSubmit={handleSubmit} />

            {/*
            <Box sx={{ textAlign: 'center' }}>
                <Link to="/register" style={{ textDecoration: 'none', color: '#1976d2' }}>
                    {"Don't have an account? Sign Up"}
                </Link>
            </Box> */}
        </Box>
    );
};

export default FormsBox;