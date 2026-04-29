/**
 * inputFields.jsx
 *
 * Small, reusable input components for the auth forms.  Each component is a
 * thin wrapper around MUI TextField with the correct name, type, and
 * autocomplete attributes pre-configured.  Refs are forwarded from the parent
 * hook so values can be read on form submission without controlled state.
 */
import {
  TextField,
  Typography,
  Checkbox,
  FormControlLabel
} from '@mui/material';
/**
 * Email input field for login and signup forms.
 * @param {React.RefObject} emailRef - Ref attached to the underlying input.
 */
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

/**
 * Password input field.  Uses type="password" so the browser masks the value.
 * @param {React.RefObject} passwordRef - Ref attached to the underlying input.
 */
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

/**
 * Username input field (signup only).
 * @param {React.RefObject} usernameRef - Ref attached to the underlying input.
 */
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