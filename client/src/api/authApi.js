import apiClient from "./axiosClient";

export const registerUserApi = async (userData) => {
    const response = await fetch(`/register`, {
        method: "POST",
        headers: {
            "content-type": "application/json"
        },
        body: JSON.stringify(userData)
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Registeration failed");
    }

    return response.json();
};

export const loginUserApi = async (userData) => {
    const response = await apiClient.post('/auth/login', userData);

    return response.data;
};