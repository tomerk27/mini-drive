import apiClient from "./axiosClient";

export const removeItemApi = async (itemId, ) => {
    const response = await apiClient.delete(`/items/remove/${itemId}`);

    return response.data;
}