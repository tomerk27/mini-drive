import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@mui/material';
import { useState } from 'react';

const CreateFolderDialog = ({ open, onClose, onCreate, isLoading }) => {
    const [folderName, setFolderName] = useState('New Folder');

    const handleCreate = () => {
        onCreate(folderName);
        setFolderName('New Folder');
    };

    const handleClose = () => {
        onClose();
        setFolderName('New Folder');
    }

    return (
        <Dialog 
            open={open} 
            onClose={handleClose}
            disableRestoreFocus
        >
            <DialogTitle>New Folder</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    label="Folder Name"
                    type="text"
                    fullWidth
                    variant="standard"
                    value={folderName}
                    onChange={(e) => setFolderName(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            handleCreate();
                        }
                    }}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose} disabled={isLoading}>Cancel</Button>
                <Button onClick={handleCreate} disabled={isLoading || !folderName.trim()}>Create</Button>
            </DialogActions>
        </Dialog>
    );
};

export default CreateFolderDialog;
