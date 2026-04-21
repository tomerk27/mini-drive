from bson import ObjectId
from typing import List, Optional, Dict, Any
from gateways.database.database import get_collection
from models.item import ItemModel, FileModel, FolderModel
from core.enums import ItemType


class ItemRepository:
    def __init__(self):
        self.collection = get_collection('items')

    def _parse_to_model(self, raw_dict: dict) -> Optional[ItemModel]:
        if not raw_dict:
            return None

        raw_dict["id"] = str(raw_dict["_id"])
        # Support both item_type and type for robustness
        item_type_val = raw_dict.get("item_type") or raw_dict.get("type")

        if item_type_val == "file":
            return FileModel(**raw_dict)
        elif item_type_val == "folder":
            return FolderModel(**raw_dict)
        else:
            return ItemModel(**raw_dict)

    async def get_by_id(self, item_id: str) -> Optional[ItemModel]:
        try:
            raw = await self.collection.find_one({"_id": ObjectId(item_id)})
            return self._parse_to_model(raw)
        except Exception:
            return None

    async def get_by_name_and_parent(self, owner_id: str, parent_id: str, name: str) -> Optional[ItemModel]:
        raw = await self.collection.find_one({
            "owner_id": owner_id,
            "parent_id": parent_id,
            "name": name
        })
        return self._parse_to_model(raw)

    async def insert(self, item: ItemModel) -> str:
        data = item.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def update(self, item_id: str, update_data: Dict[str, Any]) -> Optional[ItemModel]:
        raw = await self.collection.find_one_and_update(
            {"_id": ObjectId(item_id)},
            {"$set": update_data},
            return_document=True
        )
        return self._parse_to_model(raw)

    async def delete(self, item_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0

    async def get_children(self, parent_id: str) -> List[ItemModel]:
        cursor = self.collection.find({"parent_id": parent_id})
        raw_items = await cursor.to_list(length=1000)
        return [self._parse_to_model(raw) for raw in raw_items]

    async def update_star(self, item_id: str, user_id: str, is_starred: bool):
        op = "$pull" if is_starred else "$addToSet"
        await self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {op: {"starred_by": user_id}}
        )

    async def get_starred_items(self, user_id: str) -> List[ItemModel]:
        cursor = self.collection.find({"starred_by": user_id})
        raw_items = await cursor.to_list(length=100)
        return [self._parse_to_model(raw) for raw in raw_items]

    async def get_shared_items(self, user_id: str) -> List[ItemModel]:
        cursor = self.collection.find({"shared_with.id": user_id})
        raw_items = await cursor.to_list(length=100)
        return [self._parse_to_model(raw) for raw in raw_items]

    async def get_files_on_node(self, node_id: str) -> List[FileModel]:
        cursor = self.collection.find({
            "item_type": ItemType.FILE,
            "chunks": {"$elemMatch": {"node_ids": node_id}}
        })
        raw_items = await cursor.to_list(length=None)
        return [self._parse_to_model(raw) for raw in raw_items]

    async def replace_node_in_chunk(self, item_id: str, chunk_physical_name: str, old_node_id: str, new_node_id: str):
        await self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$pull": {"chunks.$[chunk].node_ids": old_node_id}},
            array_filters=[{"chunk.physical_name": chunk_physical_name}]
        )
        await self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$addToSet": {"chunks.$[chunk].node_ids": new_node_id}},
            array_filters=[{"chunk.physical_name": chunk_physical_name}]
        )

    async def get_used_storage(self, user_id: str) -> int:
        """Returns total bytes used by completed files owned by the user."""
        pipeline = [
            {"$match": {"owner_id": user_id, "item_type": "file", "status": "completed"}},
            {"$group": {"_id": None, "total": {"$sum": "$size"}}}
        ]
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        return result[0]["total"] if result else 0

    async def get_ancestors(self, folder_id: str) -> List[dict]:
        """Walks up parent chain and returns [{id, name}] from root-level down to folder_id."""
        ancestors = []
        current_id = folder_id


        for _ in range(20):  # safety limit for depth
            item = await self.get_by_id(current_id)
            if not item:
                break
            if not item.parent_id or item.parent_id == '/':
                # This is the root folder itself — stop without including it
                break
            ancestors.append({"id": item.id, "name": item.name})
            current_id = item.parent_id

        ancestors.reverse()
        return ancestors

    async def search(self, user_id: str, query: str) -> list[ItemModel]:
        cursor = self.collection.find({
            "$or": [
                {"owner_id": user_id},
                {"shared_with.id": user_id}
            ],
            "name": {"$regex": query, "$options": "i"}
        })

        raw_items = await cursor.to_list(length=100)
        return [self._parse_to_model(raw) for raw in raw_items]
item_repository = ItemRepository()
