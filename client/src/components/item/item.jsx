import { Card, CardActionArea, CardContent, Typography, Box, IconButton } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import FileIcon from './itemIcon';

const Item = ({ item, onClick, onOpenMenu }) => {
    const isFolder = item.item_type === 'folder' || item.type === 'folder';
    const type = isFolder ? 'folder' : item.file_type;
    const itemName = item.name;

    return (
        <Card
            sx={{
                width: '100%',
                borderRadius: 2,
                position: 'relative',
                border: '1px solid #e0e0e0',
                boxShadow: 'none',
                '&:hover': {
                    boxShadow: 2,
                    bgcolor: '#f8f9fa'
                }
            }}
        >
            <Box sx={{ position: 'absolute', top: 5, right: 5, zIndex: 10 }}>
                <IconButton
                    onClick={onOpenMenu}
                    size='small'
                >
                    <MoreVertIcon fontSize='small' />
                </IconButton>
            </Box>

            <CardActionArea 
                sx={{ height: '100%', pt: 4, pb: 2 }}
                onClick={onClick}
                onContextMenu={onOpenMenu}
            >

                <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                    <FileIcon fileType={type} />
                </Box>

                <CardContent sx={{ py: 0, px: 2 }}>
                    <Typography
                        variant="subtitle1"
                        component="div"
                        noWrap
                        title={itemName}
                        sx={{ fontWeight: 'bold', fontSize: '0.9rem' }}
                    >
                        {itemName}
                    </Typography>
                </CardContent>

            </CardActionArea>
        </Card>
    );
};

export default Item;
