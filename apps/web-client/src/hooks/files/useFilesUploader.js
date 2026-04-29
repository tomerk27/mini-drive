/**
 * Hook that manages the two-step file upload flow for multiple files.
 *
 * Exposes inputRef to wire up a hidden <input type="file"> element,
 * and uploadProgress to display a per-file progress bar while uploading.
 */

import { useState, useRef } from "react";
import { initUploadApi, uploadFileContentApi } from "../../api/fileApi";
import handleError from "../../utils/handleError";

const useFilesUploader = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    // uploadProgress: { fileName, percent (0-100), processing (true when at 100% but server is working) }
    const [uploadProgress, setUploadProgress] = useState(null);
    // inputRef is attached to the hidden file input so we can trigger it programmatically.
    const inputRef = useRef(null);

    /**
     * Uploads all selected files sequentially (one after another).
     * For each file: calls init, then uploads content with progress tracking.
     *
     * @param {Event} event - The change event from the file input.
     * @param {string} parentId - Destination folder ID.
     * @param {Function} [onUploadSuccess] - Called once all files are uploaded.
     */
    const uploadFiles = async (event, parentId, onUploadSuccess) => {
        setIsLoading(true);
        setError(null);
        setUploadProgress(null);

        const files = Array.from(event.target.files);

        if (!files.length) {
            setIsLoading(false);
            return Promise.resolve([]);
        }

        try {
            const results = [];
            for (const file of files) {
                // Show 0% progress while waiting for the server to create the record.
                setUploadProgress({ fileName: file.name, percent: 0, processing: false });
                const initData = await initUploadApi(file.name, parentId);

                // Upload content and update progress bar as bytes are sent.
                await uploadFileContentApi(initData.id, file, (percent) => {
                    // processing=true when upload is done but server-side replication is still running.
                    setUploadProgress({ fileName: file.name, percent, processing: percent === 100 });
                });
                results.push(initData);
            }

            // Reset the file input so the same file can be re-selected later.
            if (inputRef.current) {
                inputRef.current.value = null;
            }
            if (onUploadSuccess) {
                onUploadSuccess();
            }
            return results;
        } catch (error) {
            handleError(setError, error, "Failed to upload files. Please try again.");
            return Promise.reject(error);
        } finally {
            setIsLoading(false);
            setUploadProgress(null);
        }
    };

    return {
        error,
        inputRef,
        uploadFiles,
        isLoading,
        uploadProgress,
    };
};

export default useFilesUploader;