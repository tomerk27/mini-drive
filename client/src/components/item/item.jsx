import { Card, CardActionArea, CardContent, Typography, Box } from '@mui/material';
import FileIcon from './itemIcon';
import ActionMenu from './actionMenu';
import RenameDialog from './renameDialog';
import PreviewDialog from './previewDialog';
import useRenameItem from '../../hooks/itemActions/useRenameItem';
import useFilePreview from '../../hooks/useFilePreview';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Item = ({ item, refreshFolder }) => {
    const navigate = useNavigate();
    const isFolder = item.item_type === 'folder' || item.type === 'folder';
    const type = isFolder ? 'folder' : item.file_type;
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

    const handleItemClick = async () => {
        if (isFolder) {
            navigate(`/dashboard/${item.id}`);
        } else {
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
                <ActionMenu 
                    item={item} 
                    refreshFolder={refreshFolder} 
                    onRenameClick={openRenameModal} 
                />
            </Box>

            <CardActionArea 
                sx={{ height: '100%', pt: 4, pb: 2 }}
                onClick={handleItemClick}
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
