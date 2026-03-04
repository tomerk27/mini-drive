import { useState } from "react";
import { renameItemApi } from "../../api/itemApi";
import handleError from "../../utils/handleError";

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