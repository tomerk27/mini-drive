import { useState, useRef } from "react";
import { initUploadApi, uploadFileContentApi } from "../api/fileApi";

const useFilesUploader = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const inputRef = useRef(null);

    const uploadFiles = async (event, parentId) => {
        setIsLoading(true);
        setError(null);

        const files = Array.from(event.target.files);

        if (!files) {
            setIsLoading(false)
            return;
        }

        try {
            const filesPromises = files.map(async (file) => {
                const initData = await initUploadApi(file.name, parentId);
                const fileId = initData.id;
                console.log(initData)

                await uploadFileContentApi(fileId, file);

                return initData;
            });

            await Promise.all(filesPromises);

            if (inputRef.current) {
                inputRef.current.value = null;
            }
        } catch (error) {
            setError(error)
        } finally {
            setIsLoading(false);
        }
    };

    return {
        error,
        inputRef,
        uploadFiles,
        isLoading
    };
};

export default useFilesUploader;