import apiClient from "./axiosClient";

export const getStarredItemsApi = async () => {
    const response = await apiClient.get('/users/starred-items');

    return response.data;
};

export const getSharedItemsApi = async () => {
    const response = await apiClient.get('/users/shared-with-me');

    return response.data;
};

export const getStorageUsageApi = async () => {
    const response = await apiClient.get('/users/storage');

    return response.data;
};