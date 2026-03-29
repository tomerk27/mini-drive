import {  
  TextField, 
  Typography, 
  Checkbox,
  FormControlLabel
} from '@mui/material';
export const EmailField = ({ emailRef }) => {
    return (
        <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email"
            name="email"
            autoComplete="email"
            autoFocus
            inputRef={emailRef}
            size="small"
        />
    );
};

export const PasswordField = ({ passwordRef }) => {
    return (
        <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            inputRef={passwordRef}
            size="small"
        />
    );
};

export const UsernameField = ({ usernameRef }) => {
    return (
        <TextField
            margin="normal"
            required
            fullWidth
            name="username"
            label="Username"
            type="username"
            id="username"
            autoComplete="current-username"
            inputRef={usernameRef}
            size="small"
        />
    );
};

export const RememberMeField = () => {
    return (
        <FormControlLabel
            control={<Checkbox value="remember" color="primary" />}
            label={<Typography variant="body2" color="text.secondary">Remember me</Typography>}
            sx={{ mt: 1 }}
        />
    )
};