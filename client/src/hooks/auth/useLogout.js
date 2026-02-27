import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthContext } from "../../context/auth/authContext";

const useLogout = () => {
    const navigate = useNavigate();

    const { logout } = useAuthContext();

    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);


    const handleLogOut = async () => {
        setError(null);
        setIsLoading(true);

        try {
            logout();
            navigate('/login');
        } catch (error) {
            setError(error);
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