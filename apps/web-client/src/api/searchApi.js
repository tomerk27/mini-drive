/**
 * searchApi.js
 *
 * API call for full-text item search. The query is sent as a URL parameter
 * so results are shareable via the browser address bar.
 */
import apiClient from "./axiosClient";

/**
 * Searches all files and folders owned by or shared with the current user.
 *
 * @param {string} query - The search term to match against item names.
 * @returns {Promise<Object>} Object containing a list of matching items.
 */
export const searchApi = async (query) => {
    const response = await apiClient.get(`/items/search`, {
        params: { query }
    });
    return response.data;
};