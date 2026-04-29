/**
 * useStarredItems.js
 *
 * Hook that loads all items the current user has starred.  The result is
 * stored in `starredItems` and can be refreshed by calling `loadStarredItems`
 * again (e.g. after toggling a star).
 */
import { useState } from "react";
import { getStarredItemsApi } from "../../api/userApi";
import handleError from "../../utils/handleError"

/**
 * Hook for fetching the current user's starred files and folders.
 *
 * @returns {{
 *   starredItems: Object|null,
 *   loadStarredItems: () => Promise<void>,
 *   isLoading: boolean,
 *   error: string|null
 * }}
 */
const useStarredItems = () => {
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [starredItems, setStarredItems] = useState(null);

    const loadStarredItems = async () => {
        setError(null);
        setIsLoading(true);

        try {
            const items = await getStarredItemsApi();

            setStarredItems(items);
        } catch (error) {
            handleError(setError, error, "Couldn't load starred files. Please refresh the page.");
        } finally {
            setIsLoading(false);
        }
    };

    return {
        error, 
        isLoading,
        starredItems,
        loadStarredItems
    };
};

export default useStarredItems;