import pymongo
from fastapi.encoders import jsonable_encoder
from pydantic import conint
from pymongo import MongoClient

from app.core.core_config import MONGO_COLLECTION_CATEGORIES
from app.db.repositories.base import PyMongoBaseRepo
from app.schemas.schema_db import ToDoCategoryInDB


class CategoryRepository(PyMongoBaseRepo):

    def __int__(self, mongo: MongoClient):
        super().__init__(mongo)

    def list_categories(self,
                        sort_field: str = "created_at",
                        sort_order: int = pymongo.DESCENDING,
                        skip: conint(ge=0) = 0,
                        limit: conint(ge=5, multiple_of=5) = 10
                        ):
        categories = self.database[MONGO_COLLECTION_CATEGORIES] \
            .find({}) \
            .sort([(sort_field, sort_order)]) \
            .skip(skip).limit(limit)
        total = self.database[MONGO_COLLECTION_CATEGORIES].count_documents(filter={})

        return [ToDoCategoryInDB(**category) for category in categories], total

    def create_category(self, todo_category: ToDoCategoryInDB) -> ToDoCategoryInDB:
        category_in_json = jsonable_encoder(todo_category)
        new_category = self.database[MONGO_COLLECTION_CATEGORIES] \
            .insert_one(document=category_in_json)
        created_category = self.database[MONGO_COLLECTION_CATEGORIES].find_one(
            {"_id": new_category.inserted_id}
        )
        return ToDoCategoryInDB(**created_category)
