"""
Permission enforcement helpers for item-level access control.
"""

from core.enums import SharePermission
from core.exceptions import PermissionError


def verify_access(item: dict, user_id: str, action: str, required_permission: SharePermission):
    """
    Checks whether a user has the required permission on an item.

    Owners always pass. Shared users pass only if their assigned permission
    meets or exceeds the required level (VIEWER < EDITOR < OWNER).

    Args:
        item: The raw item dict from the database (must include owner_id and shared_with).
        user_id: The ID of the user requesting access.
        action: Human-readable description of the action, used in the error message.
        required_permission: The minimum permission level needed to proceed.

    Raises:
        PermissionError: If the user is not the owner and has insufficient rights.
    """
    if item.get("owner_id") == user_id:
        return  # Owners always have full access.

    # Check each entry in the shared_with list for this user.
    for user in item.get("shared_with", []):
        if user.get("id") != user_id:
            continue

        # VIEWER permission satisfies any read-level requirement.
        if required_permission == SharePermission.VIEWER:
            return

        # EDITOR permission satisfies editor-level requirements.
        if (
            required_permission == SharePermission.EDITOR
            and user.get("permission") == SharePermission.EDITOR
        ):
            return

        # User was found in shared_with but their permission is too low.
        raise PermissionError(action=action)

    # User is not the owner and not in shared_with at all.
    raise PermissionError(action=action)
