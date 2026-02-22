import { Box, Grid, Typography, CircularProgress } from '@mui/material';
import useFolder from '../../hooks/useFolder';
import Item from '../item/item';

const FolderView = () => {
    const { childFiles, childFolders, loading, error } = useFolder();

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
                        <Item fileName={item.name} fileType={item.item_type === 'FOLDER' ? 'folder' : item.file_type} />
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default FolderView;