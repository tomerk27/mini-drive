import { useState } from "react";

const useItemActionMenu = () => {
    const [anchorEl, setAnchorElement] = useState(null);
    const isOpen = Boolean(anchorEl);

    const openMenu = (event) => {
        event.stopPropagation();
        setAnchorElement(event.currentTarget);
    }

    const closeMenu = (event) => {
        if (event) event.stopPropagation();
        setAnchorElement(null);
    }

    return {
        anchorEl,
        isOpen,
        openMenu, 
        closeMenu
    };
};

export default useItemActionMenu;