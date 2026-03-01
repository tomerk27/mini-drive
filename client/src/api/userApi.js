import apiClient from "./axiosClient";

export const getStarredItemsApi = async () => {
    const response = await apiClient.get('/users/starredItems');

    return response.data;
};