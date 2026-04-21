import { Card, CardActionArea, CardContent, Typography, Box, IconButton } from '@mui/material';
import { alpha } from '@mui/material/styles';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import FileIcon from './itemIcon';

const Item = ({ item, onClick, onOpenMenu }) => {
    const isFolder = (item.item_type || item.type) === 'folder';
    const type = isFolder ? 'folder' : item.file_type;
    const itemName = item.name;

    return (
        <Card
            sx={{
                width: '100%',
                borderRadius: 4,
                position: 'relative',
                border: '1px solid #f1f5f9',
                boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
                transition: 'all 0.2s ease-in-out',
                overflow: 'hidden', // Reverted to hidden
                '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
                    borderColor: 'primary.light',
                    '& .more-icon': {
                        opacity: 1,
                    }
                }
            }}
        >
            <Box 
                className="more-icon"
                sx={{ 
                    position: 'absolute', 
                    top: 16, 
                    right: 16, 
                    zIndex: 10,
                    opacity: 0,
                    transition: 'opacity 0.2s',
                    backgroundColor: alpha('#ffffff', 0.9),
                    borderRadius: '50%',
                    backdropFilter: 'blur(4px)',
                    boxShadow: '0 2px 4px -1px rgb(0 0 0 / 0.06)'
                }}
            >
                <IconButton
                    onClick={onOpenMenu}
                    size='small'
                    sx={{ color: 'text.secondary' }}
                >
                    <MoreVertIcon fontSize='small' />
                </IconButton>
            </Box>

            <CardActionArea 
                sx={{ 
                    height: '100%', 
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'stretch',
                    p: 0,
                }}
                onClick={onClick}
                onContextMenu={onOpenMenu}
            >
                <Box 
                    sx={{ 
                        display: 'flex', 
                        justifyContent: 'center', 
                        alignItems: 'center',
                        pt: 4,
                        pb: 3,
                        backgroundColor: '#f8fafc',
                        flexGrow: 1,
                    }}
                >
                    <Box sx={{ transform: 'scale(1.2)' }}>
                        <FileIcon fileType={type} />
                    </Box>
                </Box>

                <Box sx={{ 
                    px: 2, 
                    py: 2, 
                    backgroundColor: '#ffffff', 
                    borderTop: '1px solid #f1f5f9',
                }}>
                    <Typography
                        variant="subtitle1"
                        component="div"
                        noWrap
                        title={itemName}
                        sx={{ 
                            fontWeight: 600, 
                            fontSize: '0.85rem',
                            color: 'text.primary',
                            textAlign: 'center'
                        }}
                    >
                        {itemName}
                    </Typography>
                    {item.created_at && (
                        <Typography 
                            variant="caption" 
                            sx={{ 
                                display: 'block', 
                                textAlign: 'center', 
                                color: 'text.secondary',
                                fontSize: '0.7rem',
                                mt: 0.5
                            }}
                        >
                            {new Date(item.created_at).toLocaleDateString()}
                        </Typography>
                    )}
                </Box>

            </CardActionArea>
        </Card>
    );
};

export default Item;
