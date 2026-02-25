import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@mui/material';
import { useState } from 'react';

const RenameDialog = ({ open, onClose, onRename, currentName, isRenaming }) => {
    const [newName, setNewName] = useState(currentName);

    const handleRename = () => {
        onRename(newName);
    };

    const handleClose = () => {
        onClose();
    }

    return (
        <Dialog 
        open={open} 
        onClose={handleClose}
        disableRestoreFocus
        >
            <DialogTitle>Rename</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    label="New Name"
                    type="text"
                    fullWidth
                    variant="standard"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose} disabled={isRenaming}>Cancel</Button>
                <Button onClick={handleRename} disabled={isRenaming}>Rename</Button>
            </DialogActions>
        </Dialog>
    );
};

export default RenameDialog;
