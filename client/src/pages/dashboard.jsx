import FolderView from '../components/FolderView/FolderView';
import FileUploaderBtn from '../components/fileUploader';
import useFolder from '../hooks/useFolder';

const Dashboard = () => {
    const { folder, refreshFolder } = useFolder();

    return (
        <div className="main-page">
            {folder && (
                <FileUploaderBtn 
                    currentFolderId={folder.id} 
                    onUploadSuccess={() => refreshFolder(folder.id)} 
                />
            )}
            <FolderView />
        </div>
    );
};

export default Dashboard;