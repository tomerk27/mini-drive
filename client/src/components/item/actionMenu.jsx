import { IconButton, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import DeleteIcon from '@mui/icons-material/Delete';
import ShareIcon from '@mui/icons-material/Share';
import EditIcon from '@mui/icons-material/Edit';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import useItemActionMenu from '../../hooks/useItemActionMenu';
import useRemoveItem from '../../hooks/itemActions/useRemoveItem';

const ActionMenu = ({item, refreshFolder}) => {
    const { anchorEl, isOpen, openMenu, closeMenu } = useItemActionMenu();

    const { removeItem, isRemoving } = useRemoveItem();

    const handleRemoveClick = async (event) => {
        closeMenu(event);

        await removeItem(item.id, refreshFolder);
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
                    <ListItemIcon><ShareIcon fontSize='small'>Share</ShareIcon></ListItemIcon>
                    <ListItemText>Share</ListItemText>
                </MenuItem>

                <MenuItem onClick={handleRemoveClick} disabled={isRemoving}>
                    <ListItemIcon><DeleteIcon fontSize='small'></DeleteIcon></ListItemIcon>
                    <ListItemText>Delete</ListItemText>
                </MenuItem>

                <MenuItem>
                    <ListItemIcon><EditIcon fontSize='small'></EditIcon></ListItemIcon>
                    <ListItemText>Edit</ListItemText>
                </MenuItem>
                <MenuItem>
                    <ListItemIcon><InfoOutlinedIcon fontSize='small'></InfoOutlinedIcon></ListItemIcon>
                    <ListItemText>details</ListItemText>
                </MenuItem>
            </Menu>

        </>
    )
};

export default ActionMenu;