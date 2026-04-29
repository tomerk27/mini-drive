/**
 * API calls for the two-step file upload flow and file preview.
 *
 * Upload is split into two requests:
 *   1. initUploadApi  — creates a PENDING record and returns the file ID.
 *   2. uploadFileContentApi — streams the actual bytes using multipart form data.
 */

import apiClient from "./axiosClient";

/**
 * Step 1: Creates a PENDING file record on the server and returns its ID.
 *
 * @param {string} fileName - Original filename shown in the drive.
 * @param {string} parentId - ID of the folder this file belongs to.
 * @returns {Promise<Object>} The new file item (including its id).
 */
export const initUploadApi = async (fileName, parentId) => {
    const response = await apiClient.post('/items/upload/init', {
        name: fileName,
        parent_id: parentId,
        item_type: 'file'
    });

    return response.data;
};

/**
 * Step 2: Uploads the actual file bytes to the server.
 *
 * @param {string} fileId - ID returned by initUploadApi.
 * @param {File} fileObject - The browser File object to upload.
 * @param {Function} [onProgress] - Optional callback receiving upload % (0–100).
 * @returns {Promise<Object>} The completed file item.
 */
export const uploadFileContentApi = async (fileId, fileObject, onProgress) => {
    const formData = new FormData();
    formData.append("file", fileObject);

    const response = await apiClient.post(`/items/upload/${fileId}/content`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (e) => {
            if (onProgress && e.total) {
                onProgress(Math.round((e.loaded * 100) / e.total));
            }
        },
    });

    return response.data;
};

/**
 * Downloads file content from the server as a Blob (for in-browser preview).
 *
 * @param {string} fileId - The file item ID.
 * @returns {Promise<Blob>} Raw file bytes as a Blob.
 */
export const getFileContentApi = async (fileId) => {
    const response = await apiClient.get(`/items/preview/${fileId}`, {
        responseType: 'blob'
    });

    return response.data;
};