import { useCallback, useEffect, useState } from "react"
import { useParams } from 'react-router-dom';
import { useAuthContext } from '../context/auth/authContext';
import folderApi from "../api/folderApi";

const useFolder = () => {
    const { folderId } = useParams();
    const { user } = useAuthContext();
    
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [childFiles, setChildFiles] = useState([]);
    const [childFolders, setChildFolders] = useState([]);
    const [folder, setFolder] = useState(null);

    const refreshFolder = useCallback(async (id) => {
        setLoading(true);
        setError(null);

        try {
            const data = await folderApi.getFolder(id);
            setChildFiles(data.child_files);
            setChildFolders(data.child_folders.map(folder => ({ ...folder, type: 'folder' })));
            setFolder(data.folder);
            
        } catch(error) {
            setError(error);
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
        refreshFolder 
    };
};

export default useFolder;