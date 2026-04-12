from bson import ObjectId
from typing import List, Optional, Dict, Any
from infrastructure.database.database import get_collection
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


item_repository = ItemRepository()
