import { useState, useRef } from "react";
import { filesUploaderApi } from "../api/fileApi";

const useFilesUploader = () => {
    const [files, setFiles] = useState(null);
    const inputRef = useRef(null);
    
    const handleFilesUpload = (event) => {
        setFiles(Array.from(event.target.files));
    };

    const uploadFiles = async () => {
        if(!files) return;

        await filesUploaderApi(files);

        if(inputRef.current){
            inputRef.current.value = null;
        }
        
        setFiles([]);
    };

    return { 
        inputRef, 
        handleFilesUpload, 
        uploadFiles,
    };
};

export default useFilesUploader;