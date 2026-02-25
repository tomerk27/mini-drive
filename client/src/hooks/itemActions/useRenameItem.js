import { useState } from "react";
import { renameItemApi } from "../../api/itemApi";

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
            setError(err.response?.data?.detail || "Failed to rename item");
            console.error("Renaming error: ", err);
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
        isRenameModalOpen,
        openRenameModal,
        closeRenameModal
    };
};

export default useRenameItem;