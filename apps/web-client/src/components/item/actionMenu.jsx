import { Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import ShareIcon from '@mui/icons-material/Share';
import EditIcon from '@mui/icons-material/Edit';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import useRemoveItem from '../../hooks/itemActions/useRemoveItem';
import useMarkAsStarred from '../../hooks/itemActions/useMarkAsStarred';
import { useAuthContext } from '../../context/auth/authContext';

const ActionMenu = ({
    item, 
    refreshFolder, 
    onRenameClick, 
    onDetailsClick,
    onShareClick,
    onRemoveClick,
    onStarClick,
    isRemoving,
    isStarring,
    anchorEl,
    anchorPosition,
    isOpen,
    closeMenu
}) => {
    const { user } = useAuthContext();

    const isStarred = item.starred_by?.includes(user?.sub);

    const handleRemoveClick = async (event) => {
        closeMenu(event);
        if (onRemoveClick) {
            await onRemoveClick(item.id);
        }
    };

    const handleRenameClick = () => {
        onRenameClick();
        closeMenu();
    };

    const handleDetailsClick = () => {
        onDetailsClick();
        closeMenu();
    };

    const handleShareClick = () => {
        onShareClick();
        closeMenu();
    };

    const handleStarClick = async () => {
        closeMenu();
        if (onStarClick) {
            await onStarClick(item.id);
        }
    };

    return (
        <Menu
            id='file-menu'
            anchorEl={anchorEl}
            open={isOpen}
            onClose={closeMenu}
            onClick={closeMenu}
            anchorReference={anchorPosition ? "anchorPosition" : "anchorEl"}
            anchorPosition={anchorPosition}
        >
            <MenuItem onClick={handleShareClick}>
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
    )
};

export default ActionMenu;
