import React from 'react';
import { Button, Box, CircularProgress, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload'; // וודא שיש לך @mui/icons-material
import useFilesUploader from '../hooks/useFilesUploader';

const FileUploaderBtn = ({ currentFolderId, onUploadSuccess }) => {
    const { inputRef, uploadFiles, isLoading, error } = useFilesUploader();

    const handleFileChange = async (event) => {
        await uploadFiles(event, currentFolderId);
        if (onUploadSuccess) {
            onUploadSuccess();
        }
    };

    const handleButtonClick = () => {
        inputRef.current.click();
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, alignItems: 'flex-start', mb: 2 }}>
            
            <input
                ref={inputRef}
                type="file"
                multiple
                onChange={handleFileChange}
                style={{ display: 'none' }}
            />

            <Button
                variant="contained"
                color="primary"
                onClick={handleButtonClick}
                disabled={isLoading}
                startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <CloudUploadIcon />}
                sx={{
                    borderRadius: 20,
                    textTransform: 'none',
                    fontWeight: 'bold',
                    boxShadow: 2
                }}
            >
                {isLoading ? 'Uploading...' : 'Upload File'}
            </Button>

            {error && (
                <Alert severity="error">
                    Failed to upload: {error.message}
                </Alert>
            )}
        </Box>
    );
};

export default FileUploaderBtn;