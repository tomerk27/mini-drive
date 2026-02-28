import { Box, Typography, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import CreateNewFolderIcon from '@mui/icons-material/CreateNewFolder';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import FolderView from '../components/FolderView/FolderView'
import LogoutButton from '../components/authentication/logoutButton';
import CreateFolderDialog from '../components/FolderView/createFolderDialog';
import SideBar from '../components/sideBar/sideBar';
import useFolder from '../hooks/useFolder';
import useFilesUploader from '../hooks/useFilesUploader';
import { useState } from 'react';

const Dashboard = () => {
    const { folder, refreshFolder, childFiles, childFolders, loading, error, createFolder } = useFolder();
    const { inputRef, uploadFiles } = useFilesUploader();
    const [isCreateFolderOpen, setIsCreateFolderOpen] = useState(false);
    
    // Menu state for the 'New' button
    const [anchorEl, setAnchorEl] = useState(null);
    const openMenu = Boolean(anchorEl);

    const handleNewClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleCloseMenu = () => {
        setAnchorEl(null);
    };

    const handleNewFolderClick = () => {
        handleCloseMenu();
        setIsCreateFolderOpen(true);
    };

    const handleFileUploadClick = () => {
        handleCloseMenu();
        if (inputRef.current) {
            inputRef.current.click();
        }
    };

    const handleFileChange = async (event) => {
        if (folder) {
            try {
                await uploadFiles(event, folder.id, () => refreshFolder(folder.id));
            } catch (uploadError) {
                console.error("Upload failed:", uploadError);
            }
        }
    };

    const handleCreateFolder = async (folderName) => {
        if (folder) {
            await createFolder(folderName, folder.id);
            setIsCreateFolderOpen(false);
            refreshFolder(folder.id);
        }
    };
    
    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#f8fafd' }}>
            {/* Hidden file input for uploads */}
            <input
                ref={inputRef}
                type="file"
                multiple
                onChange={handleFileChange}
                style={{ display: 'none' }}
            />

            <SideBar onNewClick={handleNewClick} />

            {/* Dropdown Menu for 'New' button */}
            <Menu
                anchorEl={anchorEl}
                open={openMenu}
                onClose={handleCloseMenu}
                PaperProps={{
                    elevation: 3,
                    sx: { width: 220, borderRadius: 2, mt: 1 }
                }}
            >
                <MenuItem onClick={handleNewFolderClick}>
                    <ListItemIcon><CreateNewFolderIcon fontSize="small" /></ListItemIcon>
                    <ListItemText>New folder</ListItemText>
                </MenuItem>
                <Box sx={{ my: 1, borderTop: '1px solid #e0e0e0' }} />
                <MenuItem onClick={handleFileUploadClick}>
                    <ListItemIcon><UploadFileIcon fontSize="small" /></ListItemIcon>
                    <ListItemText>File upload</ListItemText>
                </MenuItem>
            </Menu>

            {/* Main Content Area */}
            <Box component="main" sx={{ flexGrow: 1, pt: 10, px: 3, pb: 3, width: 'calc(100% - 256px)' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h5" sx={{ fontWeight: 400, color: '#1f1f1f' }}>
                        My Drive
                    </Typography>
                    <LogoutButton />
                </Box>

                <CreateFolderDialog 
                    open={isCreateFolderOpen}
                    onClose={() => setIsCreateFolderOpen(false)}
                    onCreate={handleCreateFolder}
                    isLoading={loading}
                />

                <Box sx={{ 
                    bgcolor: 'white', 
                    borderRadius: 4, 
                    p: 2, 
                    minHeight: 'calc(100vh - 160px)',
                    boxShadow: '0 1px 2px 0 rgba(60,64,67,0.3)'
                }}>
                    <FolderView 
                        childFiles={childFiles} 
                        childFolders={childFolders} 
                        loading={loading} 
                        error={error} 
                        refreshFolder={() => folder && refreshFolder(folder.id)}
                    />
                </Box>
            </Box>
        </Box>
    );
};

export default Dashboard;
