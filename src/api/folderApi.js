const folderApi ={
    getFolder: async (folderId) => {
        const response = await fetch(`/api/folder?folderId=${folderId}`);

        if(!response.ok) {
            throw new Error(`Folder reciving error: ${response.status}`);
        }
        return response.json();
    },

    uploadFolder: async (formData) => {
        const response = await fetch('api/folders/upload', {
            method: "POST",
            body: formData
        });

        if(!response.ok){
            throw new Error(`Folder uploading error: ${response.status}`);
        }

        return response.json();
    }
};

export default folderApi;