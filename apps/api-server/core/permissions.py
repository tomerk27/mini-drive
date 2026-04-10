from core.enums import SharePermission
from core.exceptions import PermissionError


def verify_access(item: dict, user_id: str, action: str, required_permission: SharePermission):
    """
    Checks whether a user has the required permission on an item.
    Raises PermissionError if the user is neither the owner nor a shared user
    with sufficient rights.
    """
    if item.get("owner_id") == user_id:
        return  # Owner can do everything

    for user in item.get("shared_with", []):
        if user.get("id") != user_id:
            continue

        if required_permission == SharePermission.VIEWER:
            return

        if (
            required_permission == SharePermission.EDITOR
            and user.get("permission") == SharePermission.EDITOR
        ):
            return

        raise PermissionError(action=action)

    raise PermissionError(action=action)
