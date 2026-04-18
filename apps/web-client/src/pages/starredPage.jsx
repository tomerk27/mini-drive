import { Box } from '@mui/material';
import SideBar from '../components/sideBar/sideBar';
import TopBar from '../components/topBar/topBar';
import LogoutButton from '../components/authentication/logoutButton';
import NewItemControls from '../components/newItemControls/NewItemControls';
import useStarredItems from '../hooks/items/useStarredItems';
import FolderBrowser from '../components/folderBrowser/FolderBrowser';
import useNewItemActions from '../hooks/items/useNewItemActions';
import { useEffect } from 'react';

const StarredPage = () => {
    const { error, isLoading, starredItems, loadStarredItems } = useStarredItems();
    // folderId is null — hook falls back to user's root folder
    const newItemActions = useNewItemActions(null, loadStarredItems);

    useEffect(() => {
        loadStarredItems();
    }, []);

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
            <TopBar />

            <SideBar onNewClick={newItemActions.handleNewClick} />

            <NewItemControls actions={newItemActions} />

            <Box component="main" sx={{ flexGrow: 1, pt: 12, px: 4, pb: 4, width: 'calc(100% - 256px)' }}>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', mb: 4 }}>
                    <LogoutButton />
                </Box>

                <FolderBrowser
                    rootItems={starredItems?.items}
                    rootLabel="Starred"
                    onRefresh={loadStarredItems}
                    emptyMessage="No starred items yet"
                    emptySubMessage="Starred items will appear here"
                />
            </Box>
        </Box>
    );
};

export default StarredPage;
