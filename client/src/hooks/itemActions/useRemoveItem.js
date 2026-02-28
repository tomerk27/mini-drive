import { useState } from "react";
import { removeItemApi } from "../../api/itemApi";
import handleError from "../../utils/handleError";

const useRemoveItem = () => {
    const [isRemoving, setIsRemoving] = useState(false);

    const [error, setError] = useState(null);

    const removeItem = async (itemId, onSuccess) => {
        setIsRemoving(true);
        setError(false);

        try {
            await removeItemApi(itemId);

            if (onSuccess){
                onSuccess();
            } 
        } catch (err) {
            handleError(setError, err, "Failed to remove item");
        } finally {
            setIsRemoving(false);
        }
    };

    return { removeItem, isRemoving, error };
};

export default useRemoveItem