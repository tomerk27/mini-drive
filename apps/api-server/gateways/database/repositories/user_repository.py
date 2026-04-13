from bson import ObjectId
from typing import Optional
from gateways.database.database import get_collection
from models.user import User


class UserRepository:
    def __init__(self):
        self.collection = get_collection("users")

    async def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            raw = await self.collection.find_one({"_id": ObjectId(user_id)})
            if not raw:
                return None
            raw["id"] = str(raw["_id"])
            return User(**raw)
        except Exception:
            return None

    async def get_by_email(self, email: str) -> Optional[User]:
        raw = await self.collection.find_one({"email": email})
        if not raw:
            return None
        raw["id"] = str(raw["_id"])
        return User(**raw)

    async def insert(self, user: User) -> str:
        data = user.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def update(self, user_id: str, update_data: dict) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0


user_repository = UserRepository()
