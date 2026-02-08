import { useState, useRef } from "react";
import { useNavigate } from 'react-router-dom';
import { loginUserApi, googleConectionApi } from "../../api/authApi";
import { useAuthContext } from "../../context/auth/authContext";


const useLogin = () => {
    const navigate = useNavigate();

    const { authenticate } = useAuthContext();

    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const emailRef = useRef();
    const passwordRef = useRef();

    const handleSubmit = (event, credentialResponse = null) => {
        event.preventDefault(); // Prevents page reload on form submission
        credentialResponse ? handleGoogleLogin(credentialResponse) : handleLogin();
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

            authenticate(data.access_token);

            navigate('/dashboard');
        }
        catch (error) {
            setError(error.response?.data?.detail);
        }
        finally {
            setIsLoading(false)
        }

    }

    const handleGoogleLogin = async (credentialResponse) => {
        setError(null);
        setIsLoading(true);

        const jwtToken  = credentialResponse.credential;

        try {
            const data = await googleConectionApi(jwtToken);

            authenticate(data.access_token);

            navigate('/dashboard');
        }
        catch (error) {
            setError(error.response?.data?.detail);
        }
        finally{
            setIsLoading(false);
        }
    };

    return {
        handleGoogleLogin,
        handleSubmit,
        isLoading,
        error,
        emailRef,
        passwordRef
    };
};

export default useLogin;