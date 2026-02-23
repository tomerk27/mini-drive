import FolderView from '../components/FolderView/FolderView'
import FileUploaderBtn from '../components/fileUploader';
import useFolder from '../hooks/useFolder';

const Dashboard = () => {
    const { folder, refreshFolder, childFiles, childFolders, loading, error } = useFolder();
    
    return (
        <div className="main-page">
            {folder && (
                <FileUploaderBtn 
                    currentFolderId={folder.id} 
                    onUploadSuccess={() => refreshFolder(folder.id)} 
                />
            )}
            <FolderView 
                childFiles={childFiles} 
                childFolders={childFolders} 
                loading={loading} 
                error={error} 
                refreshFolder={() => refreshFolder(folder.id)}
            />
        </div>
    );
};

export default Dashboard;