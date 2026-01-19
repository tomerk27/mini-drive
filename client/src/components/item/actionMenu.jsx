import { IconButton, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import DeleteIcon from '@mui/icons-material/Delete';
import ShareIcon from '@mui/icons-material/Share';
import EditIcon from '@mui/icons-material/Edit';
import useItemActionMenu from '../../hooks/useItemActionMenu';

const ActionMenu = () => {
    const { anchorEl, isOpen, openMenu, closeMenu} = useItemActionMenu();

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

                <MenuItem>
                    <ListItemIcon><DeleteIcon fontSize='small'></DeleteIcon></ListItemIcon>
                    <ListItemText>Delete</ListItemText>
                </MenuItem>

                <MenuItem>
                    <ListItemIcon><EditIcon fontSize='small'></EditIcon></ListItemIcon>
                    <ListItemText>Edit</ListItemText>
                </MenuItem>
            </Menu>

        </>
    )
};

export default ActionMenu;