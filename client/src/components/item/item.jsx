import { Card, CardActionArea, CardContent, Typography, Box } from '@mui/material';
import FileIcon from './itemIcon';
import ActionMenu from './actionMenu';
import RenameDialog from './renameDialog';
import PreviewDialog from './previewDialog';
import useRenameItem from '../../hooks/itemActions/useRenameItem';
import useFilePreview from '../../hooks/useFilePreview';
import { useState } from 'react';

const Item = ({ item, refreshFolder }) => {
    const type = item.item_type === 'FOLDER' ? 'folder' : item.file_type;
    const itemName = item.name;
    const [isPreviewOpen, setIsPreviewOpen] = useState(false);
    const { 
        onRenameSubmit,
        isRenaming, 
        isRenameModalOpen, 
        openRenameModal, 
        closeRenameModal 
    } = useRenameItem(item.id, refreshFolder);

    const { getFileContent, clearPreview, isLoading, error, imageUrl } = useFilePreview();

    const handlePreviewOpen = async () => {
        if (item.item_type !== 'FOLDER') {
            setIsPreviewOpen(true);
            await getFileContent(item.id);
        }
    };

    const handlePreviewClose = () => {
        setIsPreviewOpen(false);
        clearPreview();
    };

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
                <ActionMenu 
                    item={item} 
                    refreshFolder={refreshFolder} 
                    onRenameClick={openRenameModal} 
                />
            </Box>

            <CardActionArea 
                sx={{ height: '100%', pt: 4, pb: 2 }}
                onClick={handlePreviewOpen}
                disabled={item.item_type === 'FOLDER'} // Later: add folder navigation
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
            <RenameDialog
                open={isRenameModalOpen}
                onClose={closeRenameModal}
                onRename={onRenameSubmit}
                currentName={item.name}
                isRenaming={isRenaming}
            />
            <PreviewDialog
                open={isPreviewOpen}
                onClose={handlePreviewClose}
                imageUrl={imageUrl}
                isLoading={isLoading}
                error={error}
                fileName={item.name}
                fileType={item.file_type}
            />
        </Card>
    );
};

export default Item;
