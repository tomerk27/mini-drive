import { Card, CardActionArea, CardContent, Typography, Box } from '@mui/material';
import FileIcon from './itemIcon';
import ActionMenu from './actionMenu';
import RenameDialog from './renameDialog';
import useRenameItem from '../../hooks/itemActions/useRenameItem';

const Item = ({ item, refreshFolder }) => {
    const type = item.item_type === 'FOLDER' ? 'folder' : item.file_type;
    const itemName = item.name;
    const { 
        onRenameSubmit,
        isRenaming, 
        isRenameModalOpen, 
        openRenameModal, 
        closeRenameModal 
    } = useRenameItem(item.id, refreshFolder);

    return (
        <Card
            sx={{
                width: 240,
                borderRadius: 2,
                position: 'relative',
                '&:hover': {
                    boxShadow: 6
                }
            }}
        >
            <Box sx={{ position: 'absolute', top: 5, right: 5, zIndex: 10 }}>
                <ActionMenu item={item} refreshFolder={refreshFolder} onRenameClick={openRenameModal} />
            </Box>

            <CardActionArea sx={{ height: '100%', pt: 4, pb: 2 }}>

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
            <RenameDialog
                open={isRenameModalOpen}
                onClose={closeRenameModal}
                onRename={onRenameSubmit}
                currentName={item.name}
                isRenaming={isRenaming}
            />
        </Card>
    );
};

export default Item;
