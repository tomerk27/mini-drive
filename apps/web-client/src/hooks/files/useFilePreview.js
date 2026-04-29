/**
 * Hook for fetching and displaying a file preview in the browser.
 *
 * Downloads the file as a Blob and creates a temporary object URL for use in
 * <img>, <video>, or <iframe> tags. clearPreview() revokes the object URL to
 * free memory when the preview dialog closes.
 */

import { useState } from "react";
import { getFileContentApi } from "../../api/fileApi";
import handleError from "../../utils/handleError";

const useFilePreview = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);

    /**
     * Fetches the file bytes and creates a temporary browser URL for preview.
     *
     * @param {string} itemId - The file item to preview.
     */
    const getFileContent = async (itemId) => {
        setIsLoading(true);
        setError(null);

        try {
            const blob = await getFileContentApi(itemId);
            // Create a local URL the browser can load directly (e.g. in an <img> src).
            const objectUrl = URL.createObjectURL(blob);
            setImageUrl(objectUrl);
        } catch (error) {
            handleError(setError, error, "Couldn't load the file preview. The file may be unavailable.");
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Revokes the object URL and clears the preview state.
     * Call this when the preview dialog closes to avoid memory leaks.
     */
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