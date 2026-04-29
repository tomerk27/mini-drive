/**
 * Hook that loads and manages the contents of the currently viewed folder.
 *
 * Reads folderId from the URL params (via react-router). Falls back to the
 * user's root folder when no folderId is in the URL (i.e. on /dashboard).
 */

import { useCallback, useEffect, useState } from "react";
import { useParams } from 'react-router-dom';
import { useAuthContext } from '../../context/auth/authContext';
import folderApi from "../../api/folderApi";
import handleError from "../../utils/handleError";

const useFolder = () => {
    const { folderId } = useParams();
    const { user } = useAuthContext();

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [items, setItems] = useState([]);
    const [folder, setFolder] = useState(null);
    const [breadcrumb, setBreadcrumb] = useState([]);

    /** Creates a subfolder inside the currently open folder. */
    const createFolder = async (folderName, currentFolderId) => {
        setLoading(true);
        setError(null);

        try {
            await folderApi.uploadFolder(folderName, currentFolderId);
        } catch (err) {
            handleError(setError, err, "Couldn't create the folder. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    /**
     * Fetches folder metadata, children, and breadcrumb from the API.
     * Wrapped in useCallback so it can be safely listed in useEffect deps.
     */
    const refreshFolder = useCallback(async (id) => {
        setLoading(true);
        setError(null);

        try {
            const data = await folderApi.getFolder(id);
            setItems(data.children);
            setFolder(data.folder);
            setBreadcrumb(data.breadcrumb || []);
        } catch (error) {
            handleError(setError, error, "Couldn't load this folder. Please check your connection and try again.");
        } finally {
            setLoading(false);
        }
    }, []);

    // Re-fetch whenever the URL folder ID changes, or on first load (using root folder).
    useEffect(() => {
        const currentId = folderId || user?.root_folder_id;
        if (currentId) {
            refreshFolder(currentId);
        }
    }, [folderId, user?.root_folder_id, refreshFolder]);

    return {
        loading,
        error,
        items,
        folder,
        breadcrumb,
        refreshFolder,
        createFolder
    };
};

export default useFolder;