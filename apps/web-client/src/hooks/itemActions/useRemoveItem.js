/**
 * useRemoveItem.js
 *
 * Hook for deleting a file or folder.  On success it calls an optional
 * onSuccess callback so the parent component can refresh its item list.
 * Deleting a file on the API server also triggers deletion from all 3
 * storage node replicas.
 */
import { useState } from "react";
import { removeItemApi } from "../../api/itemApi";
import handleError from "../../utils/handleError";

/**
 * Hook for deleting a file or folder.
 *
 * @returns {{
 *   removeItem: (itemId: string, onSuccess?: Function) => Promise<void>,
 *   isRemoving: boolean,
 *   error: string|null,
 *   clearError: Function
 * }}
 */
const useRemoveItem = () => {
    const [isRemoving, setIsRemoving] = useState(false);
    const [error, setError] = useState(null);

    const clearError = () => {
        setError(null);
    };

    /**
     * Deletes the item and calls onSuccess if provided (e.g. to refresh the folder).
     *
     * @param {string} itemId - ID of the item to delete.
     * @param {Function} [onSuccess] - Optional callback invoked after a successful delete.
     */
    const removeItem = async (itemId, onSuccess) => {
        setIsRemoving(true);
        setError(null);

        try {
            await removeItemApi(itemId);

            if (onSuccess) {
                onSuccess();
            }
        } catch (err) {
            handleError(setError, err, "Couldn't delete this item. Please try again.");
        } finally {
            setIsRemoving(false);
        }
    };

    return { removeItem, isRemoving, error, clearError };
};

export default useRemoveItem