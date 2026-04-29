/**
 * Pre-configured Axios instance used by all API modules in this app.
 *
 * - Automatically attaches the JWT Bearer token to every request.
 * - Redirects to /login and clears the stored token on any 401 response,
 *   unless the failing request was itself a login or register call (to avoid
 *   redirect loops when credentials are wrong).
 */

import axios from "axios";

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: { 'Content-Type': 'application/json' }
});

// Request interceptor: add the saved token as a Bearer header before every request.
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error)
    }
);

// Response interceptor: handle expired/invalid tokens globally.
apiClient.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // Don't redirect on auth endpoint failures — those are just bad credentials.
        const isAuthRequest = error.config?.url?.includes('/auth/login') || error.config?.url?.includes('/auth/register');

        if (error.response && error.response.status === 401 && !isAuthRequest) {
            localStorage.removeItem('authToken');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
)

export default apiClient;