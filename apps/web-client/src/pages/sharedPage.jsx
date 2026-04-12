import { Box, Typography } from '@mui/material';
import SideBar from '../components/sideBar/sideBar';
import TopBar from '../components/topBar/topBar';
import LogoutButton from '../components/authentication/logoutButton';
import useSharedItems from '../hooks/items/useSharedItems';
import ItemsView from '../components/itemsView/itemsView';
import { useEffect } from 'react';

const SharedPage = () => {
    const { error, isLoading, sharedItems, loadSharedItems } = useSharedItems();

    useEffect(() => {
        loadSharedItems();
    }, []);

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
            <TopBar />
            
            <SideBar />

            <Box component="main" sx={{ flexGrow: 1, pt: 12, px: 4, pb: 4, width: 'calc(100% - 256px)' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
                    <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary', letterSpacing: '-0.025em' }}>
                        Shared with me
                    </Typography>
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
                    <ItemsView 
                        items={sharedItems}
                        loading={isLoading}
                        error={error}
                        refreshFolder={loadSharedItems}
                        emptyMessage="Nothing shared with you yet"
                        emptySubMessage="Items shared with you will appear here"
                    />
                </Box>
            </Box>
        </Box>
    );
};

export default SharedPage;
