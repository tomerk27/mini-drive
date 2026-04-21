import { Box } from '@mui/material';
import LogoutButton from '../components/authentication/logoutButton';
import NewItemControls from '../components/newItemControls/NewItemControls';
import SideBar from '../components/sideBar/sideBar';
import TopBar from '../components/topBar/topBar';
import FolderBrowser from '../components/folderBrowser/FolderBrowser';
import useFolder from '../hooks/folder/useFolder';
import useNewItemActions from '../hooks/items/useNewItemActions';

const Dashboard = () => {
    const { folder, refreshFolder, items } = useFolder();
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
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', mb: 4 }}>
                    <LogoutButton />
                </Box>

                <FolderBrowser
                    rootItems={items}
                    rootLabel="My Files"
                    onRefresh={() => folder && refreshFolder(folder.id)}
                    emptyMessage="This folder is empty"
                    emptySubMessage="Upload files or create folders to get started"
                />
            </Box>
        </Box>
    );
};

export default Dashboard;
