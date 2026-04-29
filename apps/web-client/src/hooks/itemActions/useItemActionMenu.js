/**
 * Hook that manages the open/closed state of an item's action menu.
 *
 * Supports two open modes:
 *   - Button click: the menu is anchored to the clicked element (anchorEl).
 *   - Right-click: the menu appears at the cursor position (anchorPosition).
 *
 * Both modes can be handled by the same MUI Menu via anchorEl / anchorPosition props.
 */

import { useState } from "react";

const useItemActionMenu = () => {
    const [anchorEl, setAnchorEl] = useState(null);
    const [anchorPosition, setAnchorPosition] = useState(null);
    const isOpen = Boolean(anchorEl) || Boolean(anchorPosition);

    /**
     * Opens the menu. Detects whether it was a right-click or a regular click
     * and sets the appropriate anchor state.
     */
    const openMenu = (event) => {
        event.stopPropagation();

        if (event.type === 'contextmenu') {
            event.preventDefault();
            // Use mouse coordinates so the menu appears under the cursor.
            setAnchorPosition({ top: event.clientY, left: event.clientX });
            setAnchorEl(null);
        } else {
            setAnchorEl(event.currentTarget);
            setAnchorPosition(null);
        }
    };

    /** Closes the menu and stops the event from bubbling (e.g. triggering folder navigation). */
    const closeMenu = (event) => {
        if (event) event.stopPropagation();
        setAnchorEl(null);
        setAnchorPosition(null);
    };

    return {
        anchorEl,
        anchorPosition,
        isOpen,
        openMenu,
        closeMenu
    };
};

export default useItemActionMenu;