import { Box, Typography } from '@mui/material';
import FolderView from '../components/FolderView/FolderView'
import Breadcrumb from '../components/FolderView/Breadcrumb'
import LogoutButton from '../components/authentication/logoutButton';
import NewItemControls from '../components/newItemControls/NewItemControls';
import SideBar from '../components/sideBar/sideBar';
import TopBar from '../components/topBar/topBar';
import useFolder from '../hooks/folder/useFolder';
import useSearch from '../hooks/search/useSearch';
import useNewItemActions from '../hooks/items/useNewItemActions';

const Dashboard = () => {
    const { folder, refreshFolder, childFiles, childFolders, loading, error, breadcrumb } = useFolder();
    const { searchTerm, searchResults, isSearching, searchError } = useSearch();
    const newItemActions = useNewItemActions(
        folder?.id,
        () => folder && refreshFolder(folder.id)
    );

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
            <TopBar />

            <SideBar onNewClick={newItemActions.handleNewClick} />

            <NewItemControls actions={newItemActions} />

            <Box component="main" sx={{ flexGrow: 1, pt: 12, px: 4, pb: 4, width: 'calc(100% - 256px)' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
                    <Breadcrumb breadcrumb={breadcrumb} />

                    {/* Display search results or loading/error states */}
                    {isSearching && <Typography>Searching...</Typography>}
                    {searchError && <Typography color="error">{searchError}</Typography>}
                    {searchTerm && searchResults.length > 0 && (
                        <Box sx={{ mt: 2 }}>
                            <Typography variant="h6">Search Results for "{searchTerm}":</Typography>
                            {searchResults.map((item) => (
                                <Typography key={item.id}>
                                    {item.name} ({item.item_type})
                                </Typography>
                            ))}
                        </Box>
                    )}
                    {searchTerm && !isSearching && !searchError && searchResults.length === 0 && <Typography>No results found for "{searchTerm}".</Typography>}

                    <LogoutButton />
                </Box>

                <Box sx={{
                    bgcolor: 'background.paper',
                    borderRadius: 4,
                    p: 3,
                    minHeight: 'calc(100vh - 200px)',
                    border: '1px solid #f1f5f9',
                    boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
                }}>
                    <FolderView
                        childFiles={childFiles}
                        childFolders={childFolders}
                        loading={loading}
                        error={error}
                        refreshFolder={() => folder && refreshFolder(folder.id)}
                    />
                </Box>
            </Box>
        </Box>
    );
};

export default Dashboard;
