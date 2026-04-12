import { useState } from "react";
import { getFileContentApi } from "../../api/fileApi";
import handleError from "../../utils/handleError";

const useFilePreview = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);

    const getFileContent = async (itemId) => {
        setIsLoading(true);
        setError(null);

        try {
            const blob = await getFileContentApi(itemId);
            const objectUrl = URL.createObjectURL(blob);
            setImageUrl(objectUrl);
        } catch (error) {
            handleError(setError, error, "Failed to show content");
        } finally {
            setIsLoading(false);
        }
    };

    const clearPreview = () => {
        if (imageUrl) {
            URL.revokeObjectURL(imageUrl);
        }
        setImageUrl(null);
        setError(null);
    };

    return {
        getFileContent,
        clearPreview,
        isLoading,
        error,
        imageUrl
    };
};

export default useFilePreview;