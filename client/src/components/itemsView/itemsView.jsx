import { Box, Typography, CircularProgress, Grid } from '@mui/material';
import Item from '../item/item';
import ActionMenu from '../item/actionMenu';
import RenameDialog from '../item/renameDialog';
import DetailsDialog from '../item/detailsDialog';
import PreviewDialog from '../item/previewDialog';
import useItemActionMenu from '../../hooks/useItemActionMenu';
import useRenameItem from '../../hooks/itemActions/useRenameItem';
import useFilePreview from '../../hooks/useFilePreview';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ItemsView = ({ 
    items, 
    loading, 
    error, 
    refreshFolder, 
    emptyMessage = "No items found",
    emptySubMessage = ""
}) => {
    const navigate = useNavigate();
    const [selectedItem, setSelectedItem] = useState(null);
    const [isDetailsOpen, setIsDetailsOpen] = useState(false);
    const [isPreviewOpen, setIsPreviewOpen] = useState(false);

    const { anchorEl, anchorPosition, isOpen, openMenu, closeMenu } = useItemActionMenu();
    const { getFileContent, clearPreview, isLoading: isPreviewLoading, error: previewError, imageUrl } = useFilePreview();

    // Setup rename logic for the currently selected item
    const { 
        onRenameSubmit, 
        isRenaming,
        isRenameModalOpen,
        openRenameModal,
        closeRenameModal
    } = useRenameItem(selectedItem?.id, refreshFolder);

    const handleOpenMenu = (event, item) => {
        setSelectedItem(item);
        openMenu(event);
    };

    const handleItemClick = async (item) => {
        const isFolder = item.item_type === 'folder' || item.type === 'folder';
        if (isFolder) {
            navigate(`/dashboard/${item.id}`);
        } else {
            setSelectedItem(item);
            setIsPreviewOpen(true);
            await getFileContent(item.id);
        }
    };

    const handlePreviewClose = () => {
        setIsPreviewOpen(false);
        clearPreview();
    };

    const handleRenameClick = () => {
        closeMenu();
        openRenameModal();
    };

    const handleDetailsClick = () => {
        closeMenu();
        setIsDetailsOpen(true);
    };

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
                        <Item 
                            item={item} 
                            onClick={() => handleItemClick(item)}
                            onOpenMenu={(e) => handleOpenMenu(e, item)}
                        />
                    </Grid>
                ))}
            </Grid>

            {selectedItem && (
                <>
                    <ActionMenu 
                        item={selectedItem}
                        refreshFolder={refreshFolder}
                        onRenameClick={handleRenameClick}
                        onDetailsClick={handleDetailsClick}
                        anchorEl={anchorEl}
                        anchorPosition={anchorPosition}
                        isOpen={isOpen}
                        closeMenu={closeMenu}
                    />
                    <RenameDialog
                        open={isRenameModalOpen}
                        onClose={closeRenameModal}
                        onRename={onRenameSubmit}
                        currentName={selectedItem.name}
                        isRenaming={isRenaming}
                    />
                    <PreviewDialog
                        open={isPreviewOpen}
                        onClose={handlePreviewClose}
                        imageUrl={imageUrl}
                        isLoading={isPreviewLoading}
                        error={previewError}
                        fileName={selectedItem.name}
                        fileType={selectedItem.file_type}
                    />
                    <DetailsDialog
                        open={isDetailsOpen}
                        onClose={() => setIsDetailsOpen(false)}
                        item={selectedItem}
                    />
                </>
            )}
        </Box>
    );
};

export default ItemsView;
