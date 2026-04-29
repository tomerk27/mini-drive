/**
 * folderApi.js
 *
 * API calls for folder operations (fetch contents, create a new folder).
 * Files within folders are handled separately by fileApi / itemApi.
 */
import apiClient from "./axiosClient";

const folderApi = {
    /**
     * Fetches a folder and its direct children by ID.
     *
     * @param {string} folderId - The folder's MongoDB document ID.
     * @returns {Promise<Object>} Folder metadata plus its child items.
     */
    getFolder: async (folderId) => {
        const response = await apiClient.get(`/items/get/${folderId}`);
        return response.data;
    },

    /**
     * Creates a new folder inside a parent folder.
     *
     * @param {string} folderName - Display name for the new folder.
     * @param {string|null} parentId - ID of the parent folder. Defaults to root ('/') if null.
     * @returns {Promise<Object>} The newly created folder document.
     */
    uploadFolder: async (folderName, parentId) => {
        const response = await apiClient.post('/items/upload/folder', {
            name: folderName,
            parent_id: parentId || '/',
            item_type: 'folder'
        });

        return response.data;
    }
};

export default folderApi;