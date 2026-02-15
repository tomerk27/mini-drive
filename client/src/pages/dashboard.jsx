//import FilesGrid from "../components/filesGrid/filesGrid";
import FileUploaderComponent from "../components/fileUploader";
import Item from "../components/item/item";
import useFolder from "../hooks/useFolder";

const Dashboard = () => {
    const { state, refreshFolder } = useFolder();

    return (
        <div className="main-page">
            <FileUploaderComponent />
            <Item fileName={'tomer'} fileType={'jpg'} />    
        </div>
    );
};

export default Dashboard;