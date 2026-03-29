import apiClient from "./axiosClient";

export const removeItemApi = async (itemId) => {
    const response = await apiClient.delete(`/items/remove/${itemId}`);

    return response.data;
};

export const renameItemApi = async (itemId, newName) => {
    const response = await apiClient.patch(`/items/rename/${itemId}`,{
        'new_name': newName
    });

    return response.data;
};

export const markAsStarredApi = async (itemId) => {
    const response = await apiClient.patch(`/items/markAsStarred/${itemId}`);

    return response.data;
};

export const shareItemApi = async (itemId, sharedEmail, permission) => {
    const response = await apiClient.post(`/items/${itemId}/share`, {
        'email': sharedEmail,
        'permission': permission
    });

    return response.data;
};