import { useState } from "react";
import { getStarredItemsApi } from "../api/userApi";
import handleError from "../utils/handleError"

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
            handleError(setError, error, "Starred files couldn't load");
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