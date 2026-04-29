import { useState, useEffect } from 'react';
import { Dialog, DialogContent, Box, CircularProgress, Typography, IconButton, AppBar, Toolbar, Button } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import TableChartOutlinedIcon from '@mui/icons-material/TableChartOutlined';
import DescriptionIcon from '@mui/icons-material/Description';
import SlideshowOutlinedIcon from '@mui/icons-material/SlideshowOutlined';
import mammoth from 'mammoth';
import * as XLSX from 'xlsx';

const PreviewDialog = ({ open, onClose, imageUrl, isLoading, error, fileName, fileType }) => {
    // { url, html } — html: null=pending, string=success, false=error
    const [officeResult, setOfficeResult] = useState({ url: null, html: false });
    const officeHtml = (isDoc || isExcel)
        ? (officeResult.url === imageUrl ? officeResult.html : null)
        : false;

    const isImage = fileType?.startsWith('image/');
    const isPdf = fileType === 'application/pdf';
    const isVideo = fileType?.startsWith('video/');
    const isAudio = fileType?.startsWith('audio/');
    const isCsv = fileType === 'text/csv';
    const isText = fileType?.startsWith('text/') ||
                   ['application/json', 'application/javascript', 'application/xml'].includes(fileType) ||
                   isCsv;

    const isExcel = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
        'application/vnd.ms-excel.sheet.macroEnabled.12',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
    ].includes(fileType);

    const isDoc = [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
        'application/vnd.ms-word.document.macroEnabled.12',
    ].includes(fileType);

    const isPresentation = [
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.template',
        'application/vnd.ms-powerpoint.presentation.macroEnabled.12',
    ].includes(fileType);

    useEffect(() => {
        if (!imageUrl || (!isDoc && !isExcel)) return;

        let cancelled = false;

        fetch(imageUrl)
            .then(r => r.arrayBuffer())
            .then(buffer => {
                if (isDoc) {
                    return mammoth.convertToHtml({ arrayBuffer: buffer }).then(r => r.value);
                }
                const wb = XLSX.read(buffer, { type: 'array' });
                const escapeHtml = s => s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
                const sheets = wb.SheetNames.map(name => {
                    const html = XLSX.utils.sheet_to_html(wb.Sheets[name]);
                    return `<h3 style="font-family:sans-serif;padding:8px 12px;margin:0;background:#f0f0f0">${escapeHtml(name)}</h3>${html}`;
                }).join('<hr/>');
                return `<style>table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:4px 8px;font-family:sans-serif;font-size:13px}</style>${sheets}`;
            })
            .then(html => { if (!cancelled) setOfficeResult({ url: imageUrl, html }); })
            .catch(() => { if (!cancelled) setOfficeResult({ url: imageUrl, html: false }); });

        return () => { cancelled = true; };
    }, [imageUrl, isDoc, isExcel]);

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

        if (isAudio) {
            return (
                <Box sx={{ width: '100%', px: 4, py: 6, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3 }}>
                    <Typography variant="subtitle1" color="text.secondary">{fileName}</Typography>
                    <Box
                        component="audio"
                        controls
                        autoPlay={false}
                        src={imageUrl}
                        sx={{ width: '100%' }}
                    >
                        Your browser does not support the audio element.
                    </Box>
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

        if (isDoc || isExcel) {
            if (officeHtml === null) return <CircularProgress />;

            if (typeof officeHtml === 'string') {
                return (
                    <Box
                        component="iframe"
                        srcDoc={officeHtml}
                        sandbox=""
                        sx={{
                            width: '100%',
                            height: 'calc(90vh - 64px)',
                            border: 'none',
                            bgcolor: 'white'
                        }}
                    />
                );
            }

            const Icon = isExcel ? TableChartOutlinedIcon : DescriptionIcon;
            const color = isExcel ? '#228B22' : '#1976d2';
            const typeLabel = isExcel ? 'Excel Spreadsheet' : 'Word Document';
            return (
                <Box sx={{ p: 8, textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <Icon sx={{ fontSize: 100, color, mb: 2 }} />
                    <Typography variant="h6" gutterBottom>{typeLabel}</Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
                        Preview failed. Download to view the content.
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

        if (isPresentation) {
            return (
                <Box sx={{ p: 8, textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <SlideshowOutlinedIcon sx={{ fontSize: 100, color: '#FF1493', mb: 2 }} />
                    <Typography variant="h6" gutterBottom>PowerPoint Presentation</Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
                        Presentations cannot be previewed in the browser. Download to open in PowerPoint.
                    </Typography>
                    <Button variant="contained" href={imageUrl} download={fileName} sx={{ bgcolor: '#FF1493', '&:hover': { bgcolor: '#FF1493', filter: 'brightness(0.9)' } }}>
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
