/**
 * Provides authentication state and helpers to the entire app via AuthContext.
 *
 * On mount, restores the user session from localStorage if a valid token exists.
 * The decoded JWT payload is stored as `user` so any component can read claims
 * like user ID and root folder ID without re-decoding the token.
 */

import { useState } from "react";
import { jwtDecode } from "jwt-decode";
import { AuthContext } from "./authContext";

export const AuthProvider = ({ children }) => {
    // Initialize user state from localStorage so the session survives page reloads.
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

    /**
     * Saves a new JWT, decodes it, and updates the user state.
     * Called after a successful login or registration.
     *
     * @param {string} newToken - The JWT returned by the API server.
     */
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

    /** Clears the stored token and user state, effectively logging the user out. */
    const logout = () => {
        localStorage.removeItem("authToken");
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, authenticate, logout }}>
            {children}
        </AuthContext.Provider>
    );
};