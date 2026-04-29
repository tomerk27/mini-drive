/**
 * Hook for in-dialog folder navigation (used by the "Move to folder" browser).
 *
 * Maintains a viewStack: an array of { label, folderId, items } frames.
 * Clicking into a subfolder pushes a new frame; navigateTo(index) pops back
 * to any previous level. This is separate from useFolder which drives the
 * main dashboard view via the URL.
 *
 * @param {Array} rootItems - Items shown at the root level of the browser.
 * @param {string} rootLabel - Display name for the root level (e.g. "My Drive").
 * @param {Function} onRefresh - Called to refresh parent state when at the root level.
 */

import { useState, useEffect, useRef } from "react";
import folderApi from "../../api/folderApi";
import handleError from "../../utils/handleError";

const useFolderBrowser = (rootItems, rootLabel, onRefresh) => {
    // viewStack[0] is always the root; each navigated subfolder adds a new frame.
    const [viewStack, setViewStack] = useState([{ label: rootLabel, folderId: null, items: [] }]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Store onRefresh in a ref so refreshCurrent always has the latest version
    // without causing the effect to re-run every render.
    const onRefreshRef = useRef(onRefresh);
    useEffect(() => {
        onRefreshRef.current = onRefresh;
    }, [onRefresh]);

    // Keep the root frame's items in sync when the parent passes new data.
    useEffect(() => {
        setViewStack(prev => {
            const updated = [...prev];
            updated[0] = { ...updated[0], items: rootItems || [] };
            return updated;
        });
    }, [rootItems]);

    /** Opens a subfolder by fetching its children and pushing a new frame onto the stack. */
    const handleFolderClick = async (item) => {
        setLoading(true);
        setError(null);

        try {
            const data = await folderApi.getFolder(item.id);
            setViewStack(prev => [...prev, { label: item.name, folderId: item.id, items: data.children }]);
        } catch (err) {
            handleError(setError, err, "Couldn't open this folder. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    /** Navigates back to a specific depth in the stack (like clicking a breadcrumb). */
    const navigateTo = (index) => {
        setViewStack(prev => prev.slice(0, index + 1));
    };

    /**
     * Refreshes the current folder's item list.
     * If at the root level, delegates to the parent's onRefresh callback instead.
     */
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
                handleError(setError, err, "Couldn't refresh the folder contents. Please try again.");
            } finally {
                setLoading(false);
            }
        } else {
            onRefreshRef.current?.();
        }
    };

    const currentItems = viewStack[viewStack.length - 1].items;

    // Build breadcrumb from the stack frames above the root (slice off index 0).
    const breadcrumb = viewStack.slice(1).map((frame, i) => ({
        id: frame.folderId,
        name: frame.label,
        index: i + 1,
    }));

    const currentFolderId = viewStack[viewStack.length - 1].folderId;

    return {
        currentItems,
        breadcrumb,
        loading,
        error,
        handleFolderClick,
        navigateTo,
        refreshCurrent,
        currentFolderId,
    };
};

export default useFolderBrowser;