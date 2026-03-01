import { Box, Typography } from '@mui/material';
import SideBar from '../components/sideBar/sideBar';
import TopBar from '../components/topBar/topBar';
import LogoutButton from '../components/authentication/logoutButton';
import useStarredItems from '../hooks/useStarredItems';
import ItemsView from '../components/itemsView/itemsView';
import { useEffect } from 'react';

const StarredPage = () => {
    const { error, isLoading, starredItems, loadStarredItems } = useStarredItems();

    useEffect(() => {
        loadStarredItems();
    }, []);

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: '#f8fafd' }}>
            <TopBar />
            
            <SideBar />

            <Box component="main" sx={{ flexGrow: 1, pt: 10, px: 3, pb: 3, width: 'calc(100% - 256px)' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h5" sx={{ fontWeight: 400, color: '#1f1f1f' }}>
                        Starred
                    </Typography>
                    <LogoutButton />
                </Box>

                <Box sx={{ 
                    bgcolor: 'white', 
                    borderRadius: 4, 
                    p: 2, 
                    minHeight: 'calc(100vh - 160px)',
                    boxShadow: '0 1px 2px 0 rgba(60,64,67,0.3)'
                }}>
                    <ItemsView 
                        items={starredItems?.starred_items}
                        loading={isLoading}
                        error={error}
                        refreshFolder={loadStarredItems}
                        emptyMessage="No starred items yet"
                        emptySubMessage="Starred items will appear here"
                    />
                </Box>
            </Box>
        </Box>
    );
};

export default StarredPage;
