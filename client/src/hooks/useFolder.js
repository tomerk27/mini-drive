import { useCallback, useEffect, useState } from "react"
import { useParams } from 'react-router-dom';
import { useAuthContext } from '../context/auth/authContext';
import folderApi from "../api/folderApi";

const useFolder = () => {
    const { folderId } = useParams();
    const { user } = useAuthContext();
    const [state, setState] = useState({
        loading: false,
        error: null,
        childFiles: [],
        childFolders: [],
        folder: []
    });

    const refreshFolder = useCallback(async () => {
        const currentId = folderId || user?.root_folder_id;

        setState(prev => ({ ...prev, loading: true }));

        try {
            const data = await folderApi.getFolder(currentId);

            setState({
                loading: false,
                error: null,
                childFiles: data.childFiles,
                childFolders: data.childFolders,
                folder: data.folder
            });
        } catch(error) {
            setState(prev => ({ ...prev, loading: false, error: error}));
        }
        
    }, [folderId]);

    useEffect(() => {
        refreshFolder();
    }, [refreshFolder, folderId])

    return {
        ...state, 
        refreshFolder 
    };
};

export default useFolder;