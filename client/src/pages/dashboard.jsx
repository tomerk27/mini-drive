import { Box, Button } from '@mui/material';
import CreateNewFolderIcon from '@mui/icons-material/CreateNewFolder';
import FolderView from '../components/FolderView/FolderView'
import FileUploaderBtn from '../components/fileUploader';
import LogoutButton from '../components/authentication/logoutButton';
import CreateFolderDialog from '../components/FolderView/createFolderDialog';
import useFolder from '../hooks/useFolder';
import { useState } from 'react';

const Dashboard = () => {
    const { folder, refreshFolder, childFiles, childFolders, loading, error, createFolder } = useFolder();
    const [isCreateFolderOpen, setIsCreateFolderOpen] = useState(false);

    const handleCreateFolder = async (folderName) => {
        await createFolder(folderName, folder.id);
        setIsCreateFolderOpen(false);
        refreshFolder(folder.id);
    };
    
    return (
        <div className="main-page">
            <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2, mb: 2 }}>
                {folder && (
                    <>
                        <FileUploaderBtn 
                            currentFolderId={folder.id} 
                            onUploadSuccess={() => refreshFolder(folder.id)} 
                        />
                        <Button
                            variant="outlined"
                            startIcon={<CreateNewFolderIcon />}
                            onClick={() => setIsCreateFolderOpen(true)}
                            sx={{
                                borderRadius: 20,
                                textTransform: 'none',
                                fontWeight: 'bold',
                                py: 0.8
                            }}
                        >
                            New Folder
                        </Button>
                    </>
                )}
                <LogoutButton />
            </Box>

            <CreateFolderDialog 
                open={isCreateFolderOpen}
                onClose={() => setIsCreateFolderOpen(false)}
                onCreate={handleCreateFolder}
                isLoading={loading}
            />

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