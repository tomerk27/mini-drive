/**
 * useSharedItems.js
 *
 * Hook that loads all items shared with the current user by other users.
 * The result is stored in `sharedItems` and can be reloaded by calling
 * `loadSharedItems` again (e.g. after creating a new item).
 */
import { useState } from "react";
import { getSharedItemsApi } from "../../api/userApi";
import handleError from "../../utils/handleError";

/**
 * Hook for fetching items shared with the current user.
 *
 * @returns {{
 *   sharedItems: Array,
 *   loadSharedItems: () => Promise<void>,
 *   isLoading: boolean,
 *   error: string|null
 * }}
 */
const useSharedItems = () => {
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [sharedItems, setSharedItems] = useState([]);

    const loadSharedItems = async () => {
        setError(null);
        setIsLoading(true);

        try {
            const items = await getSharedItemsApi();
            // The API wraps the array in an { items: [] } envelope; fall back to empty array
            setSharedItems(items.items || []);
        } catch (error) {
            handleError(setError, error, "Shared files couldn't load");
        } finally {
            setIsLoading(false);
        }
    };

    return {
        error, 
        isLoading,
        sharedItems,
        loadSharedItems
    };
};

export default useSharedItems;
