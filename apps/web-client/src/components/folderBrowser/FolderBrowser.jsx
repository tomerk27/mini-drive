/**
 * FolderBrowser.jsx
 *
 * Combines Breadcrumb navigation with ItemsView to create a full drill-down
 * folder experience.  Starts by showing `rootItems` (passed in from the parent
 * page), and fetches sub-folder contents via useFolderBrowser as the user
 * navigates deeper.
 *
 * The optional `onFolderChange` callback lets parent pages (e.g. Dashboard)
 * know which folder is currently open so they can target uploads correctly.
 */
import { Box } from '@mui/material';
import { useEffect } from 'react';
import Breadcrumb from '../FolderView/Breadcrumb';
import ItemsView from '../itemsView/itemsView';
import useFolderBrowser from '../../hooks/folder/useFolderBrowser';

/**
 * Navigable folder browser with breadcrumb trail and item grid.
 *
 * @param {Array}    rootItems      - Items to show at the top level (before any navigation).
 * @param {string}   rootLabel      - Label for the root level in the breadcrumb (e.g. "My Files").
 * @param {Function} onRefresh      - Called to reload the root item list from the parent.
 * @param {Function} [onFolderChange] - Called with (folderId, refreshFn) on navigation changes.
 * @param {boolean}  loading        - Loading state from the parent (used at root level).
 * @param {string}   [error]        - Error message from the parent (used at root level).
 * @param {string}   [emptyMessage] - Shown when the current folder has no items.
 * @param {string}   [emptySubMessage] - Secondary message shown below emptyMessage.
 */
const FolderBrowser = ({
    rootItems,
    rootLabel,
    onRefresh,
    onFolderChange,
    loading: rootLoading,
    error: rootError,
    emptyMessage,
    emptySubMessage
}) => {
    const {
        currentItems,
        breadcrumb,
        loading: navLoading,
        error: navError,
        handleFolderClick,
        navigateTo,
        refreshCurrent,
        currentFolderId,
    } = useFolderBrowser(rootItems, rootLabel, onRefresh);

    const isAtRoot = breadcrumb.length === 0;
    // At root level, show the parent's loading/error; inside subfolders use the nav state
    const loading = isAtRoot ? (rootLoading || navLoading) : navLoading;
    const error = isAtRoot ? (rootError || navError) : navError;

    useEffect(() => {
        onFolderChange?.(currentFolderId, refreshCurrent);
    }, [currentFolderId]);

    return (
        <Box>
            <Breadcrumb
                rootLabel={rootLabel}
                onRootClick={() => navigateTo(0)}
                breadcrumb={breadcrumb}
                onItemClick={(crumb) => navigateTo(crumb.index)}
            />
            <Box sx={{
                bgcolor: 'background.paper',
                borderRadius: 4,
                p: 3,
                mt: 4,
                minHeight: 'calc(100vh - 200px)',
                border: '1px solid #f1f5f9',
                boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
            }}>
                <ItemsView
                    items={currentItems}
                    loading={loading}
                    error={error}
                    refreshFolder={refreshCurrent}
                    onFolderClick={handleFolderClick}
                    emptyMessage={emptyMessage}
                    emptySubMessage={emptySubMessage}
                />
            </Box>
        </Box>
    );
};

export default FolderBrowser;
