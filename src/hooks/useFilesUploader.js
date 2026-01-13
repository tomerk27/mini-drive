import { useState, useRef } from "react";
import { filesUploaderApi } from "../api/fileApi";

const useFilesUploader = () => {
    const [files, setFiles] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const inputRef = useRef(null);

    const handleFilesUpload = (event) => {
        setFiles(Array.from(event.target.files));
    };

    const uploadFiles = async () => {
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

            setFiles([]);
        } catch (error){
            console.log("Upload failed:", error.message);
        } finally{
            setIsLoading(false);
        }
    };

    return {
        inputRef,
        handleFilesUpload,
        uploadFiles,
        isLoading
    };
};

export default useFilesUploader;