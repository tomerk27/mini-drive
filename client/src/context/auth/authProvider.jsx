import { useState } from "react";
import { jwtDecode } from "jwt-decode";
import { AuthContext } from "./authContext";

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(() => {
        const storedToken = localStorage.getItem("authToken");
        if (storedToken) {
            try {
                return jwtDecode(storedToken);
            } catch (error) {
                console.error("Token decode failed:", error);
                return null;
            }
        }
        return null;
    });

    const authenticate = (newToken) => {
        try {
            const decodedToken = jwtDecode(newToken);
            localStorage.setItem("authToken", newToken);
            setUser(decodedToken);
        } catch (error) {
            console.error("Token decode failed:", error);
            return null;
        }
    };

    const logout = () => {
        localStorage.removeItem("authToken");
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, authenticate, logout }} >
            {children}
        </AuthContext.Provider>
    )
};