import apiClient from "./axiosClient";

export const signupUserApi = async (userData) => {
    const response = await apiClient.post('/auth/register', userData);
    
    return response.data;
};

export const loginUserApi = async (userData) => {
    const response = await apiClient.post('/auth/login', userData);

    return response.data;
};

export const googleConectionApi = async (userToken) => {
    const response = await apiClient.post('/auth/googleConnection', userToken);

    return response.data;
};