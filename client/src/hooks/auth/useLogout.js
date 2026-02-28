import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthContext } from "../../context/auth/authContext";
import handleError from "../../utils/handleError";

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
            handleError(setError, error, "Logout failed. Please try again.");
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