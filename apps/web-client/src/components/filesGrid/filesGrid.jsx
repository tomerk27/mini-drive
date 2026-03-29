import FileItem from "../fileItem/fileItem";

const FilesGrid = ({ files }) => { 
    return (
        <div className="files-grid">
            {files.map((file) => (
                <FileItem key={file.name + file.lastModified} fileName={file.name} />
            ))}
        </div>
    );
};

export default FilesGrid;