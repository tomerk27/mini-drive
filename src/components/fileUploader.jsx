import useFilesUploader from "../hooks/useFilesUploader";

const FileUploaderComponent = () => {
    const {inputRef, handleFilesUpload, uploadFiles} = useFilesUploader()

    return (
        <div className="uploader-container">
            <input
                type="file"
                multiple
                onChange={handleFilesUpload}
                ref={inputRef}
            />
            <button onClick={uploadFiles}>Upload</button>
        </div>
    );
};

export default FileUploaderComponent;