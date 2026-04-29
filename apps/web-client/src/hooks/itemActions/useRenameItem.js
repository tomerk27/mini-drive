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
            if (err.response?.status === 403) {
                handleError(setError, err, "You don't have permission to rename this item.");
                closeRenameModal();
            } else {
                handleError(setError, err, "Couldn't rename this item. Please try again.");
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