import { useCallback, useEffect, useState } from "react"
import { useParams } from 'react-router-dom';
import { useAuthContext } from '../../context/auth/authContext';
import folderApi from "../../api/folderApi";
import handleError from "../../utils/handleError";

const useFolder = () => {
    const { folderId } = useParams();
    const { user } = useAuthContext();
    
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [childFiles, setChildFiles] = useState([]);
    const [childFolders, setChildFolders] = useState([]);
    const [folder, setFolder] = useState(null);

    const createFolder = async (folderName, currentFolderId) => {
        setLoading(true);
        setError(null);

        try {
            await folderApi.uploadFolder(folderName, currentFolderId);
        } catch (err) {
            handleError(setError, err, "There was a problem with folder creation");
        } finally {
            setLoading(false);
        }
    };

    const refreshFolder = useCallback(async (id) => {
        setLoading(true);
        setError(null);

        try {
            const data = await folderApi.getFolder(id);
            setChildFiles(data.child_files);
            setChildFolders(data.child_folders.map(folder => ({ ...folder, type: 'folder' })));
            setFolder(data.folder);
            
        } catch(error) {
            handleError(setError, error, "Failed to load folder content. Please try again.");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        const currentId = folderId || user?.root_folder_id;
        if(currentId) {
            refreshFolder(currentId);
        }
    }, [folderId, user?.root_folder_id, refreshFolder]);

    return {
        loading,
        error,
        childFiles,
        childFolders,
        folder,
        refreshFolder,
        createFolder
    };
};

export default useFolder;