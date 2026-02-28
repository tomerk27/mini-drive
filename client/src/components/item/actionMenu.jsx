import { IconButton, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import DeleteIcon from '@mui/icons-material/Delete';
import ShareIcon from '@mui/icons-material/Share';
import EditIcon from '@mui/icons-material/Edit';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import useItemActionMenu from '../../hooks/useItemActionMenu';
import useRemoveItem from '../../hooks/itemActions/useRemoveItem';

const ActionMenu = ({item, refreshFolder, onRenameClick, onDetailsClick}) => {
    const { anchorEl, isOpen, openMenu, closeMenu } = useItemActionMenu();
    const { removeItem, isRemoving } = useRemoveItem();

    const handleRemoveClick = async (event) => {
        closeMenu(event);
        await removeItem(item.id, refreshFolder);
    };

    const handleRenameClick = () => {
        onRenameClick();
        closeMenu();
    };

    const handleDetailsClick = () => {
        onDetailsClick();
        closeMenu();
    };

    return (
        <>
            <IconButton
                onClick={openMenu}
                size='small'
            >
                <MoreVertIcon fontSize='small' />
            </IconButton>

            <Menu
                id='file-menu'
                anchorEl={anchorEl}
                open={isOpen}
                onClose={closeMenu}
                onClick={closeMenu}
            >
                <MenuItem>
                    <ListItemIcon><ShareIcon fontSize='small' /></ListItemIcon>
                    <ListItemText>Share</ListItemText>
                </MenuItem>

                <MenuItem onClick={handleRemoveClick} disabled={isRemoving}>
                    <ListItemIcon><DeleteIcon fontSize='small' /></ListItemIcon>
                    <ListItemText>Delete</ListItemText>
                </MenuItem>

                <MenuItem onClick={handleRenameClick}>
                    <ListItemIcon><EditIcon fontSize='small' /></ListItemIcon>
                    <ListItemText>Rename</ListItemText>
                </MenuItem>
                <MenuItem onClick={handleDetailsClick}>
                    <ListItemIcon><InfoOutlinedIcon fontSize='small' /></ListItemIcon>
                    <ListItemText>Details</ListItemText>
                </MenuItem>
            </Menu>
        </>
    )
};

export default ActionMenu;
