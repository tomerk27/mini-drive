import { Box } from '@mui/material';
import { Link } from 'react-router-dom';
import { EmailField, PasswordField, RememberMeField } from './inputFields';
import SubmitButton from './submitButton';

const FormsBox = ({ handleSubmit, emailRef, passwordRef, isLoading }) => {
    return (
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ width: '100%' }}>
            <EmailField emailRef={emailRef} isLoading={isLoading} />

            <PasswordField passwordRef={passwordRef} isLoading={isLoading} />

            <RememberMeField />

            <SubmitButton isLoading={isLoading} handleSubmit={handleSubmit} />

            {/*
            <<Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                                <Link href="#" variant="body2" underline="hover" sx={{ color: 'primary.main', fontWeight: 500 }}>
                                    Don't have an account? Sign up
                                </Link>
                            </Box> */}
        </Box>
    );
};

export default FormsBox;