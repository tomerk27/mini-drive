import { Box, Typography, CircularProgress, Grid, Snackbar, Alert } from '@mui/material';
import Item from '../item/item';
import ActionMenu from '../item/actionMenu';
import RenameDialog from '../item/renameDialog';
import DetailsDialog from '../item/detailsDialog';
import PreviewDialog from '../item/previewDialog';
import ShareDialog from '../item/shareDialog';
import useItemActionMenu from '../../hooks/itemActions/useItemActionMenu';
import useRenameItem from '../../hooks/itemActions/useRenameItem';
import useShareItem from '../../hooks/itemActions/useShareItem';
import useRemoveItem from '../../hooks/itemActions/useRemoveItem';
import useMarkAsStarred from '../../hooks/itemActions/useMarkAsStarred';
import useFilePreview from '../../hooks/files/useFilePreview';
import { useState } from 'react';

const ItemsView = ({ 
    items, 
    loading, 
    error, 
    refreshFolder, 
    emptyMessage = "No items found",
    emptySubMessage = "",
    onFolderClick
}) => {
    console.log(items)
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
        closeRenameModal,
        error: renameError,
        clearError: clearRenameError
    } = useRenameItem(selectedItem?.id, refreshFolder);

    const {
        onShareSubmit,
        isSharing,
        isShareModalOpen,
        openShareModal,
        closeShareModal,
        error: shareError,
        clearError: clearShareError
    } = useShareItem(selectedItem?.id, refreshFolder);

    const {
        removeItem,
        isRemoving,
        error: removeError,
        clearError: clearRemoveError
    } = useRemoveItem();

    const {
        markAsStarred,
        isLoading: isStarring,
        error: starError,
        clearError: clearStarError
    } = useMarkAsStarred();

    const activeError = renameError || shareError || removeError || starError;

    const handleSnackbarClose = () => {
        clearRenameError();
        clearShareError();
        clearRemoveError();
        clearStarError();
    };

    const handleOpenMenu = (event, item) => {
        setSelectedItem(item);
        openMenu(event);
    };

    const handleRemoveClick = async (itemId) => {
        await removeItem(itemId, refreshFolder);
    };

    const handleStarClick = async (itemId) => {
        await markAsStarred(itemId);
        if (refreshFolder) {
            refreshFolder();
        }
    };

    const handleItemClick = async (item) => {
        const isFolder = (item.item_type || item.type) === 'folder';
        if (isFolder) {
            onFolderClick?.(item);
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

    const handleShareClick = () => {
        closeMenu();
        openShareModal();
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
                        onShareClick={handleShareClick}
                        onRemoveClick={handleRemoveClick}
                        onStarClick={handleStarClick}
                        isRemoving={isRemoving}
                        isStarring={isStarring}
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
                    <ShareDialog
                        open={isShareModalOpen}
                        onClose={closeShareModal}
                        onShare={onShareSubmit}
                        isSharing={isSharing}
                        error={shareError}
                        currentSharedWith={selectedItem.shared_with || []}
                    />
                    <PreviewDialog
                        open={isPreviewOpen}
                        onClose={handlePreviewClose}
                        imageUrl={imageUrl}
                        isLoading={isPreviewLoading}
                        error={previewError}
                        item={selectedItem}
                    />
                    <DetailsDialog
                        open={isDetailsOpen}
                        onClose={() => setIsDetailsOpen(false)}
                        item={selectedItem}
                    />
                </>
            )}

            <Snackbar
                open={Boolean(activeError)}
                autoHideDuration={6000}
                onClose={handleSnackbarClose}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert onClose={handleSnackbarClose} severity="error" variant="filled">
                    {activeError}
                </Alert>
            </Snackbar>
        </Box>
    );
};

export default ItemsView;
