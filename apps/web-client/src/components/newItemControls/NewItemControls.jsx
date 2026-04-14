import { Box, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import CreateNewFolderIcon from '@mui/icons-material/CreateNewFolder';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import CreateFolderDialog from '../FolderView/createFolderDialog';

/**
 * Renders the "Create New" dropdown menu, folder creation dialog, and hidden file input.
 * Receives all state and handlers from useNewItemActions.
 */
const NewItemControls = ({ actions }) => {
    const {
        anchorEl, openMenu, handleCloseMenu,
        handleNewFolderClick, handleFileUploadClick,
        handleFileChange, handleCreateFolder,
        isCreateFolderOpen, setIsCreateFolderOpen,
        inputRef,
    } = actions;

    return (
        <>
            <input
                ref={inputRef}
                type="file"
                multiple
                onChange={handleFileChange}
                style={{ display: 'none' }}
            />

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

            <CreateFolderDialog
                open={isCreateFolderOpen}
                onClose={() => setIsCreateFolderOpen(false)}
                onCreate={handleCreateFolder}
            />
        </>
    );
};

export default NewItemControls;
