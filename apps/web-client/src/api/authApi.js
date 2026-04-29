/**
 * authApi.js
 *
 * API calls for user authentication. Both functions return the raw response
 * data which includes `access_token` — a JWT the caller stores via AuthContext.
 */
import apiClient from "./axiosClient";

/**
 * Registers a new user account.
 *
 * @param {{ email: string, username: string, password: string }} userData
 * @returns {Promise<{ access_token: string }>} JWT for the new session.
 */
export const signupUserApi = async (userData) => {
    const response = await apiClient.post('/auth/register', userData);

    return response.data;
};

/**
 * Logs in an existing user.
 *
 * @param {{ email: string, password: string }} userData
 * @returns {Promise<{ access_token: string }>} JWT for the authenticated session.
 */
export const loginUserApi = async (userData) => {
    const response = await apiClient.post('/auth/login', userData);

    return response.data;
};

