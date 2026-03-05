import { Box, Typography, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import CreateNewFolderIcon from '@mui/icons-material/CreateNewFolder';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import FolderView from '../components/FolderView/FolderView'
import LogoutButton from '../components/authentication/logoutButton';
import CreateFolderDialog from '../components/FolderView/createFolderDialog';
import SideBar from '../components/sideBar/sideBar';
import TopBar from '../components/topBar/topBar';
import useFolder from '../hooks/useFolder';
import useFilesUploader from '../hooks/useFilesUploader';
import { useState } from 'react';

const Dashboard = () => {
    const { folder, refreshFolder, childFiles, childFolders, loading, error, createFolder } = useFolder();
    const { inputRef, uploadFiles } = useFilesUploader();
    const [isCreateFolderOpen, setIsCreateFolderOpen] = useState(false);
    
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
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
            <TopBar />
            <input
                ref={inputRef}
                type="file"
                multiple
                onChange={handleFileChange}
                style={{ display: 'none' }}
            />

            <SideBar onNewClick={handleNewClick} />

            <Menu
                anchorEl={anchorEl}
                open={openMenu}
                onClose={handleCloseMenu}
                PaperProps={{
                    elevation: 4,
                    sx: { 
                        width: 240, 
                        borderRadius: 3, 
                        mt: 1.5,
                        border: '1px solid #f1f5f9',
                        boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)'
                    }
                }}
            >
                <MenuItem onClick={handleNewFolderClick} sx={{ py: 1.5 }}>
                    <ListItemIcon><CreateNewFolderIcon fontSize="small" color="primary" /></ListItemIcon>
                    <ListItemText primary="New folder" primaryTypographyProps={{ fontWeight: 600 }} />
                </MenuItem>
                <Box sx={{ my: 0.5, borderTop: '1px solid #f1f5f9' }} />
                <MenuItem onClick={handleFileUploadClick} sx={{ py: 1.5 }}>
                    <ListItemIcon><UploadFileIcon fontSize="small" color="primary" /></ListItemIcon>
                    <ListItemText primary="File upload" primaryTypographyProps={{ fontWeight: 600 }} />
                </MenuItem>
            </Menu>

            <Box component="main" sx={{ flexGrow: 1, pt: 12, px: 4, pb: 4, width: 'calc(100% - 256px)' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
                    <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary', letterSpacing: '-0.025em' }}>
                        My Files
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
                    bgcolor: 'background.paper', 
                    borderRadius: 4, 
                    p: 3, 
                    minHeight: 'calc(100vh - 200px)',
                    border: '1px solid #f1f5f9',
                    boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
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
