import { useState } from "react";
import { removeItemApi } from "../../api/itemApi";

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
            setError(err.response?.data?.detail || "Failed to remove item");
            console.error("Deletion error: ", err);
        } finally {
            setIsRemoving(false);
        }
    };

    return { removeItem, isRemoving, error };
};

export default useRemoveItem