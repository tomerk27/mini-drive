/**
 * React context for authentication state.
 *
 * Provides { user, authenticate, logout } to any component that calls useAuthContext().
 * Wrap the app in <AuthProvider> (see authProvider.jsx) to make these available.
 */

import { createContext, useContext } from "react";

export const AuthContext = createContext(null);

/** Hook shortcut — call this in any component instead of useContext(AuthContext). */
export const useAuthContext = () => useContext(AuthContext);