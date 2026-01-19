import { useEffect, useState } from "react"
import folderApi from "../api/folderApi";
import FolderItem from "../models/folderItem";

const useFolder = (initialFolderId = 'root') => {
    const [currentFolderId, setCurrentFolderID] = useState(initialFolderId);
    const [isLoading, setLoading] = useState(false);
    const [items, setItems] = useState([]);

    const handleFolderChange = (folderId) => {
        setCurrentFolderID(folderId)
    };

    useEffect(() => {
        const loadFolder = async () => {
            setLoading(true);

            try {
                const data = folderApi.uploadFolder(currentFolderId);
                const folder = new FolderItem(data);
                setItems(folder.children);

            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        loadFolder();
    }, [currentFolderId]);

    return(
        handleFolderChange,
        items,
        isLoading
    )
};

export default useFolder;