import { useState } from "react";

const useItemActionMenu = () => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [anchorPosition, setAnchorPosition] = useState(null);
    const isOpen = Boolean(anchorEl) || Boolean(anchorPosition);

    const openMenu = (event) => {
        event.stopPropagation();
        
        if (event.type === 'contextmenu') {
            event.preventDefault();
            setAnchorPosition({ top: event.clientY, left: event.clientX });
            setAnchorEl(null);
        } else {
            setAnchorEl(event.currentTarget);
            setAnchorPosition(null);
        }
    }

    const closeMenu = (event) => {
        if (event) event.stopPropagation();
        setAnchorEl(null);
        setAnchorPosition(null);
    }

    return {
        anchorEl,
        anchorPosition,
        isOpen,
        openMenu, 
        closeMenu
    };
};

export default useItemActionMenu;