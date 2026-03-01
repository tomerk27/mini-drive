import { Box, Typography, CircularProgress, Grid } from '@mui/material';
import Item from '../item/item';

const ItemsView = ({ 
    items, 
    loading, 
    error, 
    refreshFolder, 
    emptyMessage = "No items found",
    emptySubMessage = ""
}) => {
    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', minHeight: '400px' }}>
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box sx={{ p: 2 }}>
                <Typography color="error">{error}</Typography>
            </Box>
        );
    }

    const hasItems = items && items.length > 0;

    if (!hasItems) {
        return (
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '400px' }}>
                <Typography variant="h6" color="textSecondary">{emptyMessage}</Typography>
                {emptySubMessage && <Typography variant="body2" color="textSecondary">{emptySubMessage}</Typography>}
            </Box>
        );
    }

    return (
        <Box sx={{ p: 1 }}>
            <Grid container spacing={1}>
                {items.map((item) => (
                    <Grid size={{ xs: 6, sm: 4, md: 3, lg: 2.4 }} key={item.id}>
                        <Item item={item} refreshFolder={refreshFolder}/>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default ItemsView;
