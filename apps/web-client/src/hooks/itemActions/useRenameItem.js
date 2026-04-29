/**
 * useRenameItem.js
 *
 * Hook that manages the rename dialog lifecycle and the API call.
 * On a 403 response (permission denied) the dialog is closed immediately
 * so the user isn't left staring at a broken form.
 */
import { useState } from "react";
import { renameItemApi } from "../../api/itemApi";
import handleError from "../../utils/handleError";

/**
 * Hook for renaming a file or folder.
 *
 * @param {string} itemId - ID of the item to rename.
 * @param {Function} [onSuccessCallback] - Called after a successful rename (e.g. refresh folder).
 * @returns {{
 *   onRenameSubmit: (newName: string) => Promise<void>,
 *   isRenaming: boolean,
 *   error: string|null,
 *   clearError: Function,
 *   isRenameModalOpen: boolean,
 *   openRenameModal: Function,
 *   closeRenameModal: Function
 * }}
 */
const useRenameItem = (itemId, onSuccessCallback) => {
    const [isRenaming, setIsRenaming] = useState(false);
    const [error, setError] = useState(null);
    const [isRenameModalOpen, setIsRenameModalOpen] = useState(false);

    const openRenameModal = () => {
        setIsRenameModalOpen(true);
    };

    const closeRenameModal = () => {
        setIsRenameModalOpen(false);
    };

    const clearError = () => {
        setError(null);
    };

    const _renameItem = async (newName) => {
        setIsRenaming(true);
        setError(null);

        try {
            await renameItemApi(itemId, newName);
            closeRenameModal();
            if (onSuccessCallback) {
                onSuccessCallback();
            }
        } catch (err) {
            handleError(setError, err, "Failed to rename item");
            // Close the modal on 403 — user lacks permission and retrying won't help
            if (err.response?.status === 403) {
                closeRenameModal();
            }
        } finally {
            setIsRenaming(false);
        }
    };

    const onRenameSubmit = async (newName) => {
        await _renameItem(newName);
    };

    return { 
        onRenameSubmit,
        isRenaming, 
        error,
        clearError,
        isRenameModalOpen,
        openRenameModal,
        closeRenameModal
    };
};

export default useRenameItem;