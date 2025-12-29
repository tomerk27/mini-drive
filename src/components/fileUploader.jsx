const FileUploaderComponent = ({ onUpload, onChange, inputRef }) => {
    return (
        <div className="uploader-container">
            <input
                type="file"
                multiple
                onChange={onChange}
                ref={inputRef}
            />
            <button onClick={onUpload}>Upload</button>
        </div>
    );
};

export default FileUploaderComponent;