import { useState, useRef } from "react";
import { initUploadApi, uploadFileContentApi } from "../../api/fileApi";
import handleError from "../../utils/handleError";

const useFilesUploader = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [uploadProgress, setUploadProgress] = useState(null);
    const inputRef = useRef(null);

    const uploadFiles = async (event, parentId, onUploadSuccess) => {
        setIsLoading(true);
        setError(null);
        setUploadProgress(null);

        const files = Array.from(event.target.files);

        if (!files.length) {
            setIsLoading(false);
            return Promise.resolve([]);
        }

        try {
            const results = [];
            for (const file of files) {
                setUploadProgress({ fileName: file.name, percent: 0, processing: false });
                const initData = await initUploadApi(file.name, parentId);
                await uploadFileContentApi(initData.id, file, (percent) => {
                    setUploadProgress({ fileName: file.name, percent, processing: percent === 100 });
                });
                results.push(initData);
            }

            if (inputRef.current) {
                inputRef.current.value = null;
            }
            if (onUploadSuccess) {
                onUploadSuccess();
            }
            return results;
        } catch (error) {
            handleError(setError, error, "Failed to upload files. Please try again.");
            return Promise.reject(error);
        } finally {
            setIsLoading(false);
            setUploadProgress(null);
        }
    };

    return {
        error,
        inputRef,
        uploadFiles,
        isLoading,
        uploadProgress,
    };
};

export default useFilesUploader;