/**
 * useLogin.js
 *
 * Hook that manages the login form: reads email/password via refs, calls the
 * login API, stores the returned JWT via AuthContext, then navigates to the
 * dashboard.  Exposes loading and error state for the UI to react to.
 */
import { useState, useRef } from "react";
import { useNavigate } from 'react-router-dom';
import { loginUserApi } from "../../api/authApi";
import { useAuthContext } from "../../context/auth/authContext";
import handleError from "../../utils/handleError";


/**
 * Hook for handling the login form submission.
 *
 * Uses refs instead of controlled state for the input fields to avoid
 * re-rendering the form on every keystroke.
 *
 * @returns {{
 *   handleSubmit: Function,
 *   isLoading: boolean,
 *   error: string|null,
 *   emailRef: React.RefObject,
 *   passwordRef: React.RefObject
 * }}
 */
const useLogin = () => {
    const navigate = useNavigate();

    const { authenticate } = useAuthContext();

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    // Refs read field values on submit without triggering re-renders while typing
    const emailRef = useRef();
    const passwordRef = useRef();

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        setIsLoading(true);

        const userData = {
            "email": emailRef.current.value,
            "password": passwordRef.current.value
        };

        try {
            const data = await loginUserApi(userData);
            // Store the JWT in AuthContext so all protected routes stay accessible
            authenticate(data.access_token);
            navigate('/dashboard');
        }
        catch (error) {
            handleError(setError, error, "Incorrect email or password. Please try again.");
        }
        finally {
            setIsLoading(false);
        }
    };

    return {
        handleSubmit,
        isLoading,
        error,
        emailRef,
        passwordRef
    };
};

export default useLogin;