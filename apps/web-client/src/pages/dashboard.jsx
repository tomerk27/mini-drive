/**
 * dashboard.jsx
 *
 * Main page of the app.  Displays the current folder's contents inside a
 * FolderBrowser with breadcrumb navigation.  Also handles:
 *   - Creating new folders and uploading files via NewItemControls
 *   - Legacy inline search results (search now lives on SearchPage)
 *
 * The `refreshFnRef` pattern lets child components (FolderBrowser) register
 * their own refresh function so the Dashboard can trigger a re-fetch after
 * an upload or folder creation without knowing the current folder ID directly.
 */
import { useRef, useState } from 'react';
import { Box, Typography } from '@mui/material';
import FolderBrowser from '../components/folderBrowser/FolderBrowser';
import NewItemControls from '../components/newItemControls/NewItemControls';
import SideBar from '../components/sideBar/sideBar';
import TopBar from '../components/topBar/topBar';
import useFolder from '../hooks/folder/useFolder';
import useSearch from '../hooks/search/useSearch';
import useNewItemActions from '../hooks/items/useNewItemActions';

const Dashboard = () => {
    const { folder, refreshFolder, items, loading, error } = useFolder();
    const { searchTerm, searchResults, isSearching, searchError } = useSearch();

    const [currentFolderId, setCurrentFolderId] = useState(null);
    const refreshFnRef = useRef(null);

    // Use the folder navigated to inside FolderBrowser; fall back to the root folder
    const effectiveFolderId = currentFolderId || folder?.id;

    const handleRefresh = () => {
        // Prefer the child-registered refresh so subfolder contents update correctly
        if (refreshFnRef.current) {
            refreshFnRef.current();
        } else if (folder?.id) {
            refreshFolder(folder.id);
        }
    };

    const newItemActions = useNewItemActions(effectiveFolderId, handleRefresh);

    // FolderBrowser calls this whenever the user navigates into a subfolder
    const handleFolderChange = (folderId, refresh) => {
        setCurrentFolderId(folderId);
        refreshFnRef.current = refresh;
    };

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
            <TopBar />

            <SideBar onNewClick={newItemActions.handleNewClick} />

            <NewItemControls actions={newItemActions} />

            <Box component="main" sx={{ flexGrow: 1, pt: 12, px: 4, pb: 4, width: 'calc(100% - 256px)' }}>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', mb: 4 }}>
                    {isSearching && <Typography>Searching...</Typography>}
                    {searchError && <Typography color="error">{searchError}</Typography>}
                    {searchTerm && searchResults.length > 0 && (
                        <Box>
                            <Typography variant="h6">Search Results for "{searchTerm}":</Typography>
                            {searchResults.map((item) => (
                                <Typography key={item.id}>{item.name} ({item.item_type})</Typography>
                            ))}
                        </Box>
                    )}
                    {searchTerm && !isSearching && !searchError && searchResults.length === 0 && (
                        <Typography>No results found for "{searchTerm}".</Typography>
                    )}
                </Box>

                <FolderBrowser
                    rootItems={items}
                    rootLabel="My Files"
                    onRefresh={() => folder && refreshFolder(folder.id)}
                    onFolderChange={handleFolderChange}
                    loading={loading}
                    error={error}
                    emptyMessage="This folder is empty"
                />
            </Box>
        </Box>
    );
};

export default Dashboard;
