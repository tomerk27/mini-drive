/**
 * useMarkAsStarred.js
 *
 * Hook for toggling the starred flag on a file or folder.  The API call
 * toggles the state server-side — calling it on an already-starred item
 * removes the star.  The caller is responsible for refreshing the item list
 * after a successful toggle.
 */
import { useState } from "react";
import { markAsStarredApi } from "../../api/itemApi";
import handleError from "../../utils/handleError";

/**
 * Hook for starring or un-starring a file/folder.
 *
 * @returns {{
 *   markAsStarred: (itemId: string) => Promise<void>,
 *   isLoading: boolean,
 *   error: string|null,
 *   clearError: Function
 * }}
 */
const useMarkAsStarred = () => {
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const clearError = () => {
        setError(null);
    };

    /**
     * Toggles the starred state of an item.
     *
     * @param {string} itemId - ID of the item to star or un-star.
     */
    const markAsStarred = async (itemId) => {
        setError(null);
        setIsLoading(true);

        try {
            await markAsStarredApi(itemId);
        } catch (error) {
            handleError(setError, error, "The item couldn't be starred");
        } finally {
            setIsLoading(false);
        }
    };

    return {
        error,
        isLoading,
        markAsStarred,
        clearError
    };
};

export default useMarkAsStarred;