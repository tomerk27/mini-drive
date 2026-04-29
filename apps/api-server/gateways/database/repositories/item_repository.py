"""
Data access layer for the 'items' MongoDB collection (files and folders).
"""

from bson import ObjectId
from pymongo import ReturnDocument
from typing import List, Optional, Dict, Any
from gateways.database.database import get_collection
from models.item import ItemModel, FileModel, FolderModel
from core.enums import ItemType


class ItemRepository:
    """
    Handles all reads and writes to the 'items' collection.

    Converts raw MongoDB documents into the correct model subclass
    (FileModel or FolderModel) based on the item_type field.
    """

    def __init__(self):
        self.collection = get_collection('items')

    def _parse_to_model(self, raw_dict: dict) -> Optional[ItemModel]:
        """
        Converts a raw MongoDB document into the correct item model subclass.

        Returns None if raw_dict is empty/None (e.g. document not found).
        """
        if not raw_dict:
            return None

        raw_dict["id"] = str(raw_dict["_id"])
        item_type = raw_dict.get("item_type")

        if item_type == ItemType.FILE:
            return FileModel(**raw_dict)
        elif item_type == ItemType.FOLDER:
            return FolderModel(**raw_dict)
        else:
            return ItemModel(**raw_dict)

    def get_by_id(self, item_id: str) -> Optional[ItemModel]:
        """Fetches an item by its MongoDB ObjectId. Returns None if not found."""
        try:
            raw = self.collection.find_one({"_id": ObjectId(item_id)})
            return self._parse_to_model(raw)
        except Exception:
            return None

    def get_by_name_and_parent(self, owner_id: str, parent_id: str, name: str) -> Optional[ItemModel]:
        """
        Checks whether an item with the given name already exists in a folder.

        Used to enforce unique-name-per-folder before inserting a new item.
        """
        raw = self.collection.find_one({
            "owner_id": owner_id,
            "parent_id": parent_id,
            "name": name
        })
        return self._parse_to_model(raw)

    def insert(self, item: ItemModel) -> str:
        """
        Inserts a new item document and returns the generated MongoDB ID.

        Args:
            item: The ItemModel (or subclass) to persist.

        Returns:
            The new document's _id as a string.
        """
        data = item.model_dump(by_alias=True, exclude={"id"})
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, item_id: str, update_data: Dict[str, Any]) -> Optional[ItemModel]:
        """
        Applies a partial $set update and returns the updated document.

        Using ReturnDocument.AFTER ensures callers always see the new state.
        """
        raw = self.collection.find_one_and_update(
            {"_id": ObjectId(item_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        return self._parse_to_model(raw)

    def delete(self, item_id: str) -> bool:
        """Deletes one item by ID. Returns True if a document was actually removed."""
        result = self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0

    def get_children(self, parent_id: str) -> List[ItemModel]:
        """Returns all items whose parent_id matches the given folder ID."""
        raw_items = list(self.collection.find({"parent_id": parent_id}))
        return [self._parse_to_model(raw) for raw in raw_items]

    def update_star(self, item_id: str, user_id: str, is_starred: bool):
        """
        Toggles a user's star on an item.

        Uses $pull to remove if already starred, $addToSet to add if not
        (addToSet prevents duplicates if called twice).
        """
        op = "$pull" if is_starred else "$addToSet"
        self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {op: {"starred_by": user_id}}
        )

    def get_starred_items(self, user_id: str) -> List[ItemModel]:
        """Returns up to 100 items that the user has starred."""
        raw_items = list(self.collection.find({"starred_by": user_id}).limit(100))
        return [self._parse_to_model(raw) for raw in raw_items]

    def get_shared_items(self, user_id: str) -> List[ItemModel]:
        """Returns up to 100 items that other users have shared with this user."""
        raw_items = list(self.collection.find({"shared_with.id": user_id}).limit(100))
        return [self._parse_to_model(raw) for raw in raw_items]

    def get_files_on_node(self, node_id: str) -> List[FileModel]:
        """
        Returns all files that have at least one chunk stored on the given node.

        Used by RepairService to find which files need re-replication after a node dies.
        """
        raw_items = list(self.collection.find({
            "item_type": ItemType.FILE,
            "chunks": {"$elemMatch": {"node_ids": node_id}}
        }))
        return [self._parse_to_model(raw) for raw in raw_items]

    def replace_node_in_chunk(self, item_id: str, chunk_physical_name: str, old_node_id: str, new_node_id: str):
        """
        Swaps one node ID for another within a specific chunk's node_ids list.

        Uses two separate operations: $pull to remove the old node, then $addToSet
        to add the new one. Both are filtered to the matching chunk via array_filters.
        Called by RepairService after successfully re-replicating a chunk.
        """
        self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$pull": {"chunks.$[chunk].node_ids": old_node_id}},
            array_filters=[{"chunk.physical_name": chunk_physical_name}]
        )
        self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$addToSet": {"chunks.$[chunk].node_ids": new_node_id}},
            array_filters=[{"chunk.physical_name": chunk_physical_name}]
        )

    def get_used_storage(self, user_id: str) -> int:
        """
        Returns the total bytes of all completed files owned by the user.

        Uses a MongoDB aggregation pipeline to sum the size field across
        all COMPLETED file documents owned by this user.
        """
        pipeline = [
            {"$match": {"owner_id": user_id, "item_type": "file", "status": "completed"}},
            {"$group": {"_id": None, "total": {"$sum": "$size"}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]["total"] if result else 0

    def get_ancestors(self, folder_id: str) -> List[dict]:
        """
        Walks up the folder tree and returns the breadcrumb trail.

        Iterates parent_id links until it reaches the root (no parent_id or '/').
        Capped at 20 levels to prevent infinite loops in case of data corruption.
        The result is reversed so it's ordered from root → current folder.
        """
        ancestors = []
        current_id = folder_id

        for _ in range(20):
            item = self.get_by_id(current_id)
            if not item:
                break
            if not item.parent_id or item.parent_id == '/':
                break
            ancestors.append({"id": item.id, "name": item.name})
            current_id = item.parent_id

        # Reverse to put the top-level folder first in the breadcrumb.
        ancestors.reverse()
        return ancestors

    def search(self, user_id: str, query: str) -> list[ItemModel]:
        """
        Searches items by name using a case-insensitive regex.

        Includes items owned by the user and items shared with them.
        Capped at 100 results.
        """
        raw_items = list(self.collection.find({
            "$or": [
                {"owner_id": user_id},
                {"shared_with.id": user_id}
            ],
            "name": {"$regex": query, "$options": "i"}
        }).limit(100))
        return [self._parse_to_model(raw) for raw in raw_items]


# Singleton instance used across the entire API server process.
item_repository = ItemRepository()
