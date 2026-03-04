import { useState } from "react";
import { shareItemApi } from "../../api/itemApi";
import handleError from "../../utils/handleError";

const useShareItem = (itemId, onSuccessCallback) => {
    const [isSharing, setIsSharing] = useState(false);
    const [error, setError] = useState(null);
    const [isShareModalOpen, setIsShareModalOpen] = useState(false);

    const openShareModal = () => {
        setIsShareModalOpen(true);
    };

    const closeShareModal = () => {
        setIsShareModalOpen(false);
    };

    const clearError = () => {
        setError(null);
    };

    const onShareSubmit = async (email, permission) => {
        setIsSharing(true);
        setError(null);

        try {
            await shareItemApi(itemId, email, permission);
            closeShareModal();
            if (onSuccessCallback) {
                onSuccessCallback();
            }
        } catch (err) {
            handleError(setError, err, "Failed to share item");
            if (err.response?.status === 403) {
                closeShareModal();
            }
        } finally {
            setIsSharing(false);
        }
    };

    return { 
        onShareSubmit,
        isSharing, 
        error,
        clearError,
        isShareModalOpen,
        openShareModal,
        closeShareModal
    };
};

export default useShareItem;
