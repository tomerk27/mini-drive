import { IconButton, Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import DeleteIcon from '@mui/icons-material/Delete';
import ShareIcon from '@mui/icons-material/Share';
import EditIcon from '@mui/icons-material/Edit';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import useItemActionMenu from '../../hooks/useItemActionMenu';
import useRemoveItem from '../../hooks/itemActions/useRemoveItem';
import useMarkAsStarred from '../../hooks/itemActions/useMarkAsStarred';
import { useAuthContext } from '../../context/auth/authContext';

const ActionMenu = ({item, refreshFolder, onRenameClick, onDetailsClick}) => {
    const { anchorEl, isOpen, openMenu, closeMenu } = useItemActionMenu();
    const { removeItem, isRemoving } = useRemoveItem();
    const { markAsStarred, isLoading: isStarring } = useMarkAsStarred();
    const { user } = useAuthContext();

    const isStarred = item.starred_by?.includes(user?.sub);

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

    const handleStarClick = async () => {
        closeMenu();
        await markAsStarred(item.id);
        if (refreshFolder) {
            refreshFolder();
        }
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

                <MenuItem onClick={handleStarClick} disabled={isStarring}>
                    <ListItemIcon>
                        {isStarred ? <StarIcon fontSize='small' sx={{ color: '#FFD700' }} /> : <StarBorderIcon fontSize='small' />}
                    </ListItemIcon>
                    <ListItemText>{isStarred ? 'Remove Star' : 'Star'}</ListItemText>
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
