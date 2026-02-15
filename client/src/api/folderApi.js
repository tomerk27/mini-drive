import apiClient from "./axiosClient";

const folderApi = {
    getFolder: async (folderId) => {
        const response = await apiClient.get(`/api/folder?folderId=${folderId}`);

        return response.data;
    },

    uploadFolder: async (folderName, parentId) => {
        const response = await apiClient('/items/upload/folder', {
            name: folderName,
            parent_id: parentId || '/',
            item_type: 'folder'
        });

        return response.data;
    }
};

export default folderApi;