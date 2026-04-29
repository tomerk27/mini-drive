/**
 * userApi.js
 *
 * API calls for user-level data: starred items, items shared with the current
 * user, and storage quota usage. All endpoints require a valid JWT (attached
 * automatically by axiosClient).
 */
import apiClient from "./axiosClient";

/**
 * Fetches all items the current user has starred.
 *
 * @returns {Promise<{ items: Array }>} Object with an `items` array.
 */
export const getStarredItemsApi = async () => {
    const response = await apiClient.get('/users/starred-items');

    return response.data;
};

/**
 * Fetches all items that other users have shared with the current user.
 *
 * @returns {Promise<{ items: Array }>} Object with an `items` array.
 */
export const getSharedItemsApi = async () => {
    const response = await apiClient.get('/users/shared-with-me');

    return response.data;
};

/**
 * Fetches the current user's storage usage and quota.
 *
 * @returns {Promise<{ used: number, max: number }>} Bytes used and total quota.
 */
export const getStorageUsageApi = async () => {
    const response = await apiClient.get('/users/storage');

    return response.data;
};