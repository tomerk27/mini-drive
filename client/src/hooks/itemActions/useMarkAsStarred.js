import { useState } from "react";
import { markAsStarredApi } from "../../api/itemApi";
import handleError from "../../utils/handleError";

const useMarkAsStarred = () => {
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

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
        markAsStarred
    };
};

export default useMarkAsStarred;