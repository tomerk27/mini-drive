import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, Box, Divider } from '@mui/material';
import FileIcon from './itemIcon';

const DetailsDialog = ({ open, onClose, item }) => {
    if (!item) return null;

    const isFolder = item.item_type === 'folder' || item.type === 'folder';
    const type = isFolder ? 'folder' : item.file_type;

    const formatDate = (dateString) => {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        return date.toLocaleString();
    };

    const formatSize = (bytes) => {
        if (bytes === 0 || !bytes) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth disableRestoreFocus>
            <DialogTitle sx={{ fontWeight: 'bold' }}>Item Details</DialogTitle>
            <DialogContent dividers>
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
                    <FileIcon fileType={type} />
                    <Typography variant="h6" sx={{ mt: 1, fontWeight: 'medium', wordBreak: 'break-all', textAlign: 'center' }}>
                        {item.name}
                    </Typography>
                </Box>

                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <Box>
                        <Typography variant="caption" color="text.secondary" display="block">
                            Type
                        </Typography>
                        <Typography variant="body2">
                            {isFolder ? 'Folder' : item.file_type.split('/')[1] || 'Unknown File'}
                        </Typography>
                    </Box>

                    {!isFolder && (
                        <Box>
                            <Typography variant="caption" color="text.secondary" display="block">
                                Size
                            </Typography>
                            <Typography variant="body2">
                                {formatSize(item.size)}
                            </Typography>
                        </Box>
                    )}

                    <Box>
                        <Typography variant="caption" color="text.secondary" display="block">
                            Created At
                        </Typography>
                        <Typography variant="body2">
                            {formatDate(item.created_at)}
                        </Typography>
                    </Box>

                    <Box>
                        <Typography variant="caption" color="text.secondary" display="block">
                            Owner
                        </Typography>
                        <Typography variant="body2">
                            {item.is_owner ? 'Me' : 'Shared with me'}
                        </Typography>
                    </Box>
                    
                    <Box>
                        <Typography variant="caption" color="text.secondary" display="block">
                            Item ID
                        </Typography>
                        <Typography variant="body2">
                            {item.id}
                        </Typography>
                    </Box>
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary">
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default DetailsDialog;
