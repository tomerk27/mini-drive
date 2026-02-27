import apiClient from "./axiosClient";

export const initUploadApi = async (fileName, parentId) => {
    const response = await apiClient.post('/items/upload/init', {
        name: fileName,
        parent_id: parentId,
        item_type: 'file'
    });

    return response.data;
};

export const uploadFileContentApi = async (fileId, fileObject) => {
    const formData = new FormData();

    formData.append("file", fileObject);

    const response = await apiClient.post(`/items/upload/${fileId}/content`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });

    return response.data
};

export const getFileContentApi = async (fileId) => {
    const response = await apiClient.get(`/items/preview/${fileId}`, {
        responseType: 'blob'
    });

    return response.data;
};