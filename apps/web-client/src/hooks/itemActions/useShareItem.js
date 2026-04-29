/**
 * useShareItem.js
 *
 * Hook that manages the share dialog and the API call for granting another
 * user access to an item.  Supports viewer and editor permission levels.
 * Like useRenameItem, a 403 response closes the modal immediately.
 */
import { useState } from "react";
import { shareItemApi } from "../../api/itemApi";
import handleError from "../../utils/handleError";

/**
 * Hook for sharing a file or folder with another user.
 *
 * @param {string} itemId - ID of the item to share.
 * @param {Function} [onSuccessCallback] - Called after a successful share (e.g. refresh folder).
 * @returns {{
 *   onShareSubmit: (email: string, permission: string) => Promise<void>,
 *   isSharing: boolean,
 *   error: string|null,
 *   clearError: Function,
 *   isShareModalOpen: boolean,
 *   openShareModal: Function,
 *   closeShareModal: Function
 * }}
 */
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
            if (err.response?.status === 403) {
                handleError(setError, err, "You don't have permission to share this item. Only the owner can share it.");
                closeShareModal();
            } else if (err.response?.status === 404) {
                handleError(setError, err, "The user you're trying to share with doesn't exist.");
            } else {
                handleError(setError, err, "Couldn't share this item. Check the email address and try again.");
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
