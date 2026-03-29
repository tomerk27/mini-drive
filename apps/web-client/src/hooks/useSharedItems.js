import { useState } from "react";
import { getSharedItemsApi } from "../api/userApi";
import handleError from "../utils/handleError";

const useSharedItems = () => {
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [sharedItems, setSharedItems] = useState([]);

    const loadSharedItems = async () => {
        setError(null);
        setIsLoading(true);

        try {
            const items = await getSharedItemsApi();
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
