import { useState, useRef } from "react";
import { useNavigate } from 'react-router-dom';
import { loginUserApi } from "../../api/authApi";
import { useAuthContext } from "../../context/auth/authContext";

const useLogin = () => {
    const navigate = useNavigate();

    const { login } = useAuthContext();

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const emailRef = useRef();
    const passwordRef = useRef();

    const handleSubmit = (event) => {
        event.preventDefault(); // Prevents page reload on form submission
        handleLogin();
    };

    const handleLogin = async () => {
        setError(null)
        setIsLoading(true);

        const userData = { 
            "email": emailRef.current.value, 
            "password": passwordRef.current.value 
        };

        try {
            const data = await loginUserApi(userData);

            login(data.access_token);

            navigate('/dashboard');
        }
        catch (error) {
            setError(error.response?.data?.detail);
        }
        finally {
            setIsLoading(false)
        }

    }

    return {
        handleSubmit,
        isLoading,
        error,
        emailRef,
        passwordRef
    };
};

export default useLogin;