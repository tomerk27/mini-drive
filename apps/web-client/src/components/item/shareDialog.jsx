import { 
    Button, 
    Dialog, 
    DialogActions, 
    DialogContent, 
    DialogTitle, 
    TextField, 
    MenuItem, 
    Select, 
    FormControl, 
    InputLabel,
    Box,
    Typography,
    List,
    ListItem,
    ListItemText,
    CircularProgress
} from '@mui/material';
import { useState } from 'react';

const ShareDialog = ({ open, onClose, onShare, isSharing, currentSharedWith = [] }) => {
    const [email, setEmail] = useState('');
    const [permission, setPermission] = useState('viewer');

    const handleShare = () => {
        if (email.trim()) {
            onShare(email, permission);
            setEmail('');
        }
    };

    const handleClose = () => {
        setEmail('');
        onClose();
    };

    return (
        <Dialog 
            open={open} 
            onClose={handleClose}
            fullWidth
            maxWidth="xs"
            disableRestoreFocus
        >
            <DialogTitle>Share Item</DialogTitle>
            <DialogContent>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
                    <TextField
                        autoFocus
                        label="User Email"
                        type="email"
                        fullWidth
                        variant="outlined"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <FormControl fullWidth>
                        <InputLabel id="permission-label">Permission</InputLabel>
                        <Select
                            labelId="permission-label"
                            value={permission}
                            label="Permission"
                            onChange={(e) => setPermission(e.target.value)}
                        >
                            <MenuItem value="viewer">Viewer</MenuItem>
                            <MenuItem value="editor">Editor</MenuItem>
                        </Select>
                    </FormControl>
                </Box>

                {currentSharedWith.length > 0 && (
                    <Box sx={{ mt: 3 }}>
                        <Typography variant="subtitle2" color="textSecondary">
                            People with access:
                        </Typography>
                        <List dense>
                            {currentSharedWith.map((user, index) => (
                                <ListItem key={index}>
                                    <ListItemText 
                                        primary={user.email || user.id} 
                                        secondary={user.permission} 
                                    />
                                </ListItem>
                            ))}
                        </List>
                    </Box>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose} disabled={isSharing}>Cancel</Button>
                <Button 
                    onClick={handleShare} 
                    disabled={isSharing || !email.trim()}
                    variant="contained"
                >
                    {isSharing ? <CircularProgress size={24} color="inherit" /> : 'Share'}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ShareDialog;
