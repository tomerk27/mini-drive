/**
 * Hook for the "New" button that lets users upload files or create folders.
 *
 * Determines the effective destination folder: uses the current URL folder if
 * present, otherwise falls back to the user's root folder. After a successful
 * action, either calls onRefresh (inside a subfolder) or navigates to /dashboard.
 *
 * @param {string|null} folderId - Current folder from URL params, or null at root.
 * @param {Function} onRefresh - Callback to reload the current folder's contents.
 */

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

    // Use the URL folder ID if available, otherwise upload to the root folder.
    const effectiveFolderId = folderId || user?.root_folder_id;

    // After uploading or creating a folder: refresh if inside a subfolder, else go to dashboard.
    const afterAction = folderId ? onRefresh : () => navigate('/dashboard');

    const handleNewClick = (event) => setAnchorEl(event.currentTarget);
    const handleCloseMenu = () => setAnchorEl(null);

    const handleNewFolderClick = () => {
        handleCloseMenu();
        setIsCreateFolderOpen(true);
    };

    /** Closes the menu and programmatically triggers the hidden file input. */
    const handleFileUploadClick = () => {
        handleCloseMenu();
        inputRef.current?.click();
    };

    /** Triggered when the user picks files — delegates to useFilesUploader. */
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
