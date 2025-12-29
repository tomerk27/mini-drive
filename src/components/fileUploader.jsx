import { useFilesUploader } from "../hooks/files.js";
const FileUploaderComponent = () => {
    const {
        inputRef, 
        handleFileChange, 
        uploadFiles
    } = useFilesUploader()
    return (
        <>
            <input
                type="file"
                multiple
                onChange={handleFileChange}
                ref={inputRef}
            />
            <button onClick={uploadFiles}>Upload</button>
        </>
    );
};

export default FileUploaderComponent;