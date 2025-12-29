import { useState, useRef } from "react";
import { filesUploaderApi } from "../api/fileApi";

export const useFilesUploader = () => {
    const [files, setFiles] = useState(null);
    const [allUploadedFiles, setAllUploadedFiles] = useState([]);
    const inputRef = useRef(null);
    
    const handleFileChange = (event) => {
        setFiles(Array.from(event.target.files));
    };

    const uploadFiles = async () => {
        if(!files) return;

        setAllUploadedFiles(prev => [...prev, ...files]);
        await filesUploaderApi(files);

        if(inputRef.current){
            inputRef.current.value = null;
        }

        const updatedList = [...allUploadedFiles, ...files]
        console.log(updatedList);

        setFiles([])
    };

    return { 
        inputRef, 
        handleFileChange, 
        uploadFiles
    };
};