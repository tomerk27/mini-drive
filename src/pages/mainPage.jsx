//import FilesGrid from "../components/filesGrid/filesGrid";
import FileUploaderComponent from "../components/fileUploader";

const MainPage = () => {
    return (
        <div className="main-page">
            <h1>My Drive</h1>

            <FileUploaderComponent />
            
        </div>
    );
};

export default MainPage;