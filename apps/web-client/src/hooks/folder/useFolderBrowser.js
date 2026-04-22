import { useState, useEffect } from "react";
import folderApi from "../../api/folderApi";
import handleError from "../../utils/handleError";

const useFolderBrowser = (rootItems, rootLabel, onRefresh) => {
    const [viewStack, setViewStack] = useState([{ label: rootLabel, folderId: null, items: [] }]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        setViewStack(prev => {
            const updated = [...prev];
            updated[0] = { ...updated[0], items: rootItems || [] };
            return updated;
        });
    }, [rootItems]);

    const handleFolderClick = async (item) => {
        setLoading(true);
        setError(null);

        try {
            const data = await folderApi.getFolder(item.id);
            setViewStack(prev => [...prev, { label: item.name, folderId: item.id, items: data.children }]);
        } catch (err) {
            handleError(setError, err, "Failed to open folder");
        } finally {
            setLoading(false);
        }
    };

    const navigateTo = (index) => {
        setViewStack(prev => prev.slice(0, index + 1));
    };

    const refreshCurrent = async () => {
        const current = viewStack[viewStack.length - 1];

        if (current.folderId) {
            setLoading(true);
            setError(null);
            try {
                const data = await folderApi.getFolder(current.folderId);
                setViewStack(prev => {
                    const updated = [...prev];
                    updated[updated.length - 1] = { ...updated[updated.length - 1], items: data.children };
                    return updated;
                });
            } catch (err) {
                handleError(setError, err, "Failed to refresh folder");
            } finally {
                setLoading(false);
            }
        } else {
            onRefresh?.();
        }
    };

    const currentItems = viewStack[viewStack.length - 1].items;
    const breadcrumb = viewStack.slice(1).map((frame, i) => ({
        id: frame.folderId,
        name: frame.label,
        index: i + 1,
    }));

    return {
        currentItems,
        breadcrumb,
        loading,
        error,
        handleFolderClick,
        navigateTo,
        refreshCurrent,
    };
};

export default useFolderBrowser;