import apiClient from "./axiosClient";

export const searchApi = async (query) => {
    const response = await apiClient.get(`/items/search`, {
        params: { query }
    });
    return response.data;
};