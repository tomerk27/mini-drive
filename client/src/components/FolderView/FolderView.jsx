import { Box, Grid, Typography, CircularProgress } from '@mui/material';
import Item from '../item/item';

const FolderView = ({ childFiles, childFolders, loading, error, refreshFolder}) => {
    const items = [...childFolders, ...childFiles];

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        console.error(error);
        return <Typography color="error">Failed to load folder.</Typography>;
    }

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                My Drive
            </Typography>
            <Grid container spacing={1}>
                {items.map((item) => (
                    <Grid size={{ xs: 6, sm: 4, md: 3, lg: 2 }} key={item.id}>
                        <Item item={item} refreshFolder={refreshFolder}/>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default FolderView;