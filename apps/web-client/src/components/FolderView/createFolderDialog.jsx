/**
 * createFolderDialog.jsx
 *
 * Modal dialog for creating a new folder.  The folder name field is
 * pre-filled with "New Folder" so the user can accept it immediately or
 * type a custom name.  Pressing Enter triggers creation without needing
 * to click the button.
 */
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@mui/material';
import { useState } from 'react';

/**
 * Dialog for naming and confirming a new folder.
 *
 * @param {boolean}  open      - Whether the dialog is visible.
 * @param {Function} onClose   - Called when the user cancels or closes.
 * @param {Function} onCreate  - Called with the folder name string on confirm.
 * @param {boolean}  isLoading - Disables buttons while the creation request is in flight.
 */
const CreateFolderDialog = ({ open, onClose, onCreate, isLoading }) => {
    const [folderName, setFolderName] = useState('New Folder');

    const handleCreate = () => {
        onCreate(folderName);
        // Reset to the default name so the next open starts fresh
        setFolderName('New Folder');
    };

    const handleClose = () => {
        onClose();
        // Reset so a previously-typed name doesn't persist on next open
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
