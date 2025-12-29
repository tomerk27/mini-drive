import FilesGrid from "../components/filesGrid/filesGrid";
import FileUploaderComponent from "../components/fileUploader";
import { useFilesUploader } from "../hooks/files";

const MainPage = () => {
    const { allUploadedFiles, uploadFiles, handleFileChange, inputRef } = useFilesUploader();

    return (
        <div className="main-page">
            <h1>My Drive</h1>

            <FileUploaderComponent 
                onUpload={uploadFiles} 
                onChange={handleFileChange} 
                inputRef={inputRef} 
            />
            
            <FilesGrid files={allUploadedFiles} />
        </div>
    );
};

export default MainPage;