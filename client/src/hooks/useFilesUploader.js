import { useState, useRef } from "react";
import { filesUploaderApi } from "../api/fileApi";

const useFilesUploader = () => {
    const [isLoading, setIsLoading] = useState(false);

    const inputRef = useRef(null);

    const uploadFiles = async (event) => {
        const files = Array.from(event.target.files);
        
        if (!files) return;

        setIsLoading(true);

        const formData = new FormData();

        files.forEach(file => {
            formData.append("file", file);
        });

        try {
            await filesUploaderApi(formData);

            if (inputRef.current) {
                inputRef.current.value = null;
            }
        } catch (error) {
            console.log("Upload failed:", error.message);
        } finally {
            setIsLoading(false);
        }
    };

    return {
        inputRef,
        uploadFiles,
        isLoading
    };
};

export default useFilesUploader;