from bson import ObjectId
from pymongo import ReturnDocument
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
        item_type = raw_dict.get("item_type")

        if item_type == ItemType.FILE:
            return FileModel(**raw_dict)
        elif item_type == ItemType.FOLDER:
            return FolderModel(**raw_dict)
        else:
            return ItemModel(**raw_dict)

    def get_by_id(self, item_id: str) -> Optional[ItemModel]:
        try:
            raw = self.collection.find_one({"_id": ObjectId(item_id)})
            return self._parse_to_model(raw)
        except Exception:
            return None

    def get_by_name_and_parent(self, owner_id: str, parent_id: str, name: str) -> Optional[ItemModel]:
        raw = self.collection.find_one({
            "owner_id": owner_id,
            "parent_id": parent_id,
            "name": name
        })
        return self._parse_to_model(raw)

    def insert(self, item: ItemModel) -> str:
        data = item.model_dump(by_alias=True, exclude={"id"})
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, item_id: str, update_data: Dict[str, Any]) -> Optional[ItemModel]:
        raw = self.collection.find_one_and_update(
            {"_id": ObjectId(item_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
        return self._parse_to_model(raw)

    def delete(self, item_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0

    def get_children(self, parent_id: str) -> List[ItemModel]:
        raw_items = list(self.collection.find({"parent_id": parent_id}))
        return [self._parse_to_model(raw) for raw in raw_items]

    def update_star(self, item_id: str, user_id: str, is_starred: bool):
        op = "$pull" if is_starred else "$addToSet"
        self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {op: {"starred_by": user_id}}
        )

    def get_starred_items(self, user_id: str) -> List[ItemModel]:
        raw_items = list(self.collection.find({"starred_by": user_id}).limit(100))
        return [self._parse_to_model(raw) for raw in raw_items]

    def get_shared_items(self, user_id: str) -> List[ItemModel]:
        raw_items = list(self.collection.find({"shared_with.id": user_id}).limit(100))
        return [self._parse_to_model(raw) for raw in raw_items]

    def get_files_on_node(self, node_id: str) -> List[FileModel]:
        raw_items = list(self.collection.find({
            "item_type": ItemType.FILE,
            "chunks": {"$elemMatch": {"node_ids": node_id}}
        }))
        return [self._parse_to_model(raw) for raw in raw_items]

    def replace_node_in_chunk(self, item_id: str, chunk_physical_name: str, old_node_id: str, new_node_id: str):
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
        pipeline = [
            {"$match": {"owner_id": user_id, "item_type": "file", "status": "completed"}},
            {"$group": {"_id": None, "total": {"$sum": "$size"}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]["total"] if result else 0

    def get_ancestors(self, folder_id: str) -> List[dict]:
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

        ancestors.reverse()
        return ancestors

    def search(self, user_id: str, query: str) -> list[ItemModel]:
        raw_items = list(self.collection.find({
            "$or": [
                {"owner_id": user_id},
                {"shared_with.id": user_id}
            ],
            "name": {"$regex": query, "$options": "i"}
        }).limit(100))
        return [self._parse_to_model(raw) for raw in raw_items]


item_repository = ItemRepository()
