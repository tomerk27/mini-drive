/**
 * @file protectedRoute.jsx
 * Route-level authentication guard. Wraps any routes that require a logged-in
 * user. If no JWT session is found in AuthContext the visitor is redirected to
 * the login page before the protected page ever renders.
 */

import { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../context/auth/authContext';

/**
 * Auth guard component used in the React Router tree.
 *
 * Reads the current user from AuthContext (populated after a successful JWT
 * login). If the user is not authenticated, redirects to /login using
 * `replace` so the protected URL is not left in the browser history.
 * Otherwise, renders the matched child route via <Outlet />.
 *
 * @returns {JSX.Element} Either a <Navigate> redirect or the child <Outlet>.
 */
const ProtectedRoute = () => {
    const { user } = useContext(AuthContext);

    // No user in context means the JWT is missing or expired — send to login.
    if (!user) {
        return <Navigate to="/login" replace />;
    }

    // User is authenticated; render whatever child route was matched.
    return <Outlet />;
};

export default ProtectedRoute;