"""
Data access layer for the 'users' MongoDB collection.
"""

from bson import ObjectId
from typing import Optional
from gateways.database.database import get_collection
from models.user import User


class UserRepository:
    """
    Handles all reads and writes to the 'users' collection.

    Every method converts the raw MongoDB dict into a User model before
    returning, keeping the rest of the codebase free of BSON types.
    """

    def __init__(self):
        self.collection = get_collection("users")

    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Fetches a user by their MongoDB ObjectId string.

        Returns None (instead of raising) if the ID is invalid or not found,
        so callers can handle missing users gracefully.
        """
        try:
            raw = self.collection.find_one({"_id": ObjectId(user_id)})
            if not raw:
                return None
            raw["id"] = str(raw["_id"])
            return User(**raw)
        except Exception:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        """Fetches a user by email address. Returns None if not found."""
        raw = self.collection.find_one({"email": email})
        if not raw:
            return None
        raw["id"] = str(raw["_id"])
        return User(**raw)

    def insert(self, user: User) -> str:
        """
        Inserts a new user document and returns the new ID as a string.

        Args:
            user: The User model to persist. The id field is excluded because
                  MongoDB generates it automatically.
        """
        data = user.model_dump(by_alias=True, exclude={"id"})
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, user_id: str, update_data: dict) -> bool:
        """
        Applies a partial update ($set) to a user document.

        Args:
            user_id: The user to update.
            update_data: Dict of fields to set (e.g. {"root_id": "..."}).

        Returns:
            True if at least one document was modified, False otherwise.
        """
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0


# Singleton instance used across the entire API server process.
user_repository = UserRepository()
