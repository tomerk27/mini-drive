/**
 * useLogout.js
 *
 * Hook for logging out the current user.  Clears the JWT from AuthContext and
 * redirects to the login page.  Exposes loading and error state so the logout
 * button can show a spinner or an error message.
 */
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthContext } from "../../context/auth/authContext";
import handleError from "../../utils/handleError";

/**
 * Hook for handling user logout.
 *
 * @returns {{
 *   handleLogOut: Function,
 *   isLoading: boolean,
 *   error: string|null
 * }}
 */
const useLogout = () => {
    const navigate = useNavigate();

    const { logout } = useAuthContext();

    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleLogOut = async () => {
        setError(null);
        setIsLoading(true);

        try {
            // Clears the JWT from context and localStorage (handled inside logout())
            logout();
            navigate('/login');
        } catch (error) {
            handleError(setError, error, "Sign out failed. Please refresh the page and try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return {
        error,
        isLoading,
        handleLogOut
    }
};

export default useLogout;