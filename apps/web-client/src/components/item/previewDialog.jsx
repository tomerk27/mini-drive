import { Dialog, DialogContent, Box, CircularProgress, Typography, IconButton, AppBar, Toolbar } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import TableChartOutlinedIcon from '@mui/icons-material/TableChartOutlined';
import DescriptionIcon from '@mui/icons-material/Description';
import { Button } from '@mui/material';

const PreviewDialog = ({ open, onClose, imageUrl, isLoading, error, item }) => {
    if (!item) return null;
    
    const fileName = item.name;
    const fileType = item.file_type;
    
    const isImage = fileType?.startsWith('image/');
    const isPdf = fileType === 'application/pdf';
    const isVideo = fileType?.startsWith('video/');
    const isCsv = fileType === 'text/csv';
    const isText = fileType?.startsWith('text/') || 
                   ['application/json', 'application/javascript', 'application/xml'].includes(fileType) ||
                   isCsv;
    
    const isExcel = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel'
    ].includes(fileType);

    const isDoc = [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword'
    ].includes(fileType);

    const renderContent = () => {
        if (isLoading) return <CircularProgress />;
        if (error) return (
            <Box sx={{ p: 4, textAlign: 'center' }}>
                <Typography color="error">{error}</Typography>
            </Box>
        );
        if (!imageUrl) return null;

        if (isImage) {
            return (
                <Box
                    component="img"
                    src={imageUrl}
                    alt={fileName}
                    sx={{
                        maxWidth: '100%',
                        maxHeight: 'calc(90vh - 64px)',
                        objectFit: 'contain',
                        display: 'block'
                    }}
                />
            );
        }

        if (isVideo) {
            return (
                <Box
                    component="video"
                    controls
                    src={imageUrl}
                    sx={{
                        maxWidth: '100%',
                        maxHeight: 'calc(90vh - 64px)',
                        bgcolor: 'black'
                    }}
                >
                    Your browser does not support the video tag.
                </Box>
            );
        }

        if (isPdf) {
            return (
                <Box
                    component="embed"
                    src={imageUrl}
                    type="application/pdf"
                    sx={{
                        width: '100%',
                        height: 'calc(90vh - 64px)',
                        border: 'none'
                    }}
                />
            );
        }

        if (isText) {
            return (
                <Box
                    component="iframe"
                    src={imageUrl}
                    sx={{
                        width: '100%',
                        height: 'calc(90vh - 64px)',
                        border: 'none',
                        bgcolor: 'white'
                    }}
                />
            );
        }

        if (isExcel || isDoc) {
            const Icon = isExcel ? TableChartOutlinedIcon : DescriptionIcon;
            const color = isExcel ? '#228B22' : '#1976d2';
            const typeLabel = isExcel ? 'Excel Spreadsheet' : 'Word Document';

            return (
                <Box sx={{ p: 8, textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <Icon sx={{ fontSize: 100, color: color, mb: 2 }} />
                    <Typography variant="h6" gutterBottom>
                        {typeLabel}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
                        Browsers cannot render this file type directly. Please download it to view the content.
                    </Typography>
                    <Button 
                        variant="contained" 
                        href={imageUrl} 
                        download={fileName}
                        sx={{ bgcolor: color, '&:hover': { bgcolor: color, filter: 'brightness(0.9)' } }}
                    >
                        Download {fileName}
                    </Button>
                </Box>
            );
        }

        return (
            <Box sx={{ p: 4, textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <InsertDriveFileIcon sx={{ fontSize: 80, color: '#909090', mb: 2 }} />
                <Typography variant="body1" sx={{ mb: 2 }}>
                    Preview is not available for this file type ({fileType}).
                </Typography>
                <Button variant="outlined" href={imageUrl} download={fileName}>
                    Download and view
                </Button>
            </Box>
        );
    };

    return (
        <Dialog 
            open={open} 
            onClose={onClose} 
            maxWidth="md" 
            fullWidth
            disableRestoreFocus
            slotProps={{
                paper: {
                    sx: { 
                        borderRadius: 2,
                        minHeight: '400px',
                        display: 'flex',
                        flexDirection: 'column'
                    }
                }
            }}
        >
            <AppBar sx={{ position: 'relative', bgcolor: 'white', color: 'black', boxShadow: 1 }}>
                <Toolbar variant="dense">
                    <Typography sx={{ ml: 2, flex: 1, fontWeight: 'bold' }} variant="subtitle1">
                        {fileName}
                    </Typography>
                    <IconButton
                        edge="start"
                        color="inherit"
                        onClick={onClose}
                        aria-label="close"
                    >
                        <CloseIcon />
                    </IconButton>
                </Toolbar>
            </AppBar>
            <DialogContent 
                sx={{ 
                    display: 'flex', 
                    justifyContent: 'center', 
                    alignItems: 'center', 
                    p: 0,
                    bgcolor: '#f5f5f5',
                    flexGrow: 1
                }}
            >
                {renderContent()}
            </DialogContent>
        </Dialog>
    );
};

export default PreviewDialog;