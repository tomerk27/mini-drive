import { useState, useRef } from "react";
import { useNavigate } from 'react-router-dom';
import { loginUserApi } from "../../api/authApi";
import { useAuthContext } from "../../context/auth/authContext";
import handleError from "../../utils/handleError";


const useLogin = () => {
    const navigate = useNavigate();

    const { authenticate } = useAuthContext();

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

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
            authenticate(data.access_token);
            navigate('/dashboard');
        }
        catch (error) {
            handleError(setError, error, "Invalid email or password");
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