import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthContext } from '../../context/auth/authContext';
import useFilesUploader from '../files/useFilesUploader';
import folderApi from '../../api/folderApi';

const useNewItemActions = (folderId, onRefresh) => {
    const { user } = useAuthContext();
    const navigate = useNavigate();
    const { inputRef, uploadFiles, uploadProgress } = useFilesUploader();

    const [anchorEl, setAnchorEl] = useState(null);
    const [isCreateFolderOpen, setIsCreateFolderOpen] = useState(false);

    const openMenu = Boolean(anchorEl);
    const effectiveFolderId = folderId || user?.root_folder_id;

    const afterAction = folderId ? onRefresh : () => navigate('/dashboard');

    const handleNewClick = (event) => setAnchorEl(event.currentTarget);
    const handleCloseMenu = () => setAnchorEl(null);

    const handleNewFolderClick = () => {
        handleCloseMenu();
        setIsCreateFolderOpen(true);
    };

    const handleFileUploadClick = () => {
        handleCloseMenu();
        inputRef.current?.click();
    };

    const handleFileChange = async (event) => {
        if (effectiveFolderId) {
            try {
                await uploadFiles(event, effectiveFolderId, afterAction);
            } catch (err) {
                console.error('Upload failed:', err);
            }
        }
    };

    const handleCreateFolder = async (folderName) => {
        if (effectiveFolderId) {
            await folderApi.uploadFolder(folderName, effectiveFolderId);
            setIsCreateFolderOpen(false);
            afterAction();
        }
    };

    return {
        anchorEl,
        openMenu,
        handleNewClick,
        handleCloseMenu,
        handleNewFolderClick,
        handleFileUploadClick,
        handleFileChange,
        handleCreateFolder,
        isCreateFolderOpen,
        setIsCreateFolderOpen,
        inputRef,
        uploadProgress,
    };
};

export default useNewItemActions;
