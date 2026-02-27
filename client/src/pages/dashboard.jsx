import { Box } from '@mui/material';
import FolderView from '../components/FolderView/FolderView'
import FileUploaderBtn from '../components/fileUploader';
import LogoutButton from '../components/authentication/logoutButton';
import useFolder from '../hooks/useFolder';

const Dashboard = () => {
    const { folder, refreshFolder, childFiles, childFolders, loading, error } = useFolder();
    
    return (
        <div className="main-page">
            <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2, mb: 2 }}>
                {folder && (
                    <FileUploaderBtn 
                        currentFolderId={folder.id} 
                        onUploadSuccess={() => refreshFolder(folder.id)} 
                    />
                )}
                <LogoutButton />
            </Box>
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