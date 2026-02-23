import { useState, useRef } from "react";
import { initUploadApi, uploadFileContentApi } from "../api/fileApi";

const useFilesUploader = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const inputRef = useRef(null);

    const uploadFiles = async (event, parentId, onUploadSuccess) => {
        setIsLoading(true);
        setError(null);

        const files = Array.from(event.target.files);

        if (!files.length) {
            setIsLoading(false)
            return Promise.resolve([]);
        }

        try {
            const filesPromises = files.map(async (file) => {
                const initData = await initUploadApi(file.name, parentId);
                const fileId = initData.id;

                await uploadFileContentApi(fileId, file);

                return initData;
            });

            const settledPromises = await Promise.all(filesPromises);

            if (inputRef.current) {
                inputRef.current.value = null;
            }
            if (onUploadSuccess) {
                onUploadSuccess();
            }
            return settledPromises;
        } catch (error) {
            setError(error);
            // Propagate the error to the caller
            return Promise.reject(error);
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