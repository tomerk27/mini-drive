/**
 * API calls for item actions: delete, rename, star, and share.
 */

import apiClient from "./axiosClient";

/** Permanently deletes an item and all its storage node chunks. */
export const removeItemApi = async (itemId) => {
    const response = await apiClient.delete(`/items/remove/${itemId}`);
    return response.data;
};

/** Renames an item. Requires at least EDITOR permission. */
export const renameItemApi = async (itemId, newName) => {
    const response = await apiClient.patch(`/items/rename/${itemId}`, {
        'new_name': newName
    });
    return response.data;
};

/**
 * Toggles the star on an item for the current user.
 * Calling this twice will unstar the item (server-side toggle).
 */
export const markAsStarredApi = async (itemId) => {
    const response = await apiClient.patch(`/items/markAsStarred/${itemId}`);
    return response.data;
};

/**
 * Shares an item with another user by email.
 *
 * @param {string} itemId - The item to share.
 * @param {string} sharedEmail - Email address of the user to share with.
 * @param {string} permission - 'viewer' or 'editor'.
 */
export const shareItemApi = async (itemId, sharedEmail, permission) => {
    const response = await apiClient.post(`/items/${itemId}/share`, {
        'email': sharedEmail,
        'permission': permission
    });
    return response.data;
};