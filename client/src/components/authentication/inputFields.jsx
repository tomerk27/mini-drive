import { TextField } from "@mui/material";

export const EmailField = ({ emailRef, isLoading }) => {
    return (
        <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            autoFocus

            inputRef={emailRef}
            disabled={isLoading}
        />
    );
};

export const PasswordField = ({ passwordRef, isLoading }) => {
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
            disabled={isLoading}
        />
    );
};