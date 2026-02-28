import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { signupUserApi } from "../../api/authApi";
import { useAuthContext } from "../../context/auth/authContext";
import handleError from "../../utils/handleError";

const useSignup = () => {
    const navigate = useNavigate();

    const { authenticate } = useAuthContext();

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const emailRef = useRef();
    const usernameRef = useRef();
    const passwordRef = useRef();

    const handleSubmit = (event) => {
        event.preventDefault(); // Prevents page reload on form submission
        handleSignup();
    };

    const handleSignup = async () => {
        setIsLoading(true);
        setError(null);

        const userData = {
            "email": emailRef.current.value,
            "username": usernameRef.current.value,
            "password": passwordRef.current.value
        };

        try{
            const data = await signupUserApi(userData);

            authenticate(data.access_token);
            
            navigate('/dashboard');
        }
        catch (error) {
            handleError(setError, error, "Sign up failed. Please check your inputs.");
        }
        finally{
            setIsLoading(false);
        }
    };

    return {
        handleSubmit,
        isLoading,
        error,
        emailRef,
        usernameRef,
        passwordRef
    };
};

export default useSignup;