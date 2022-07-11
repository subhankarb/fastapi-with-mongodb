import pymongo
from fastapi.encoders import jsonable_encoder
from pydantic import conint
from pymongo import MongoClient

from app.core.core_config import MONGO_COLLECTION_TODOS
from app.db.repositories.base import PyMongoBaseRepo
from app.schemas.schema_db import ToDoItemInDB, PyObjectId


class TodoRepository(PyMongoBaseRepo):

    def __int__(self, mongo: MongoClient):
        super().__init__(mongo)

    def list_todo(self,
                  sort_field: str = "created_at",
                  sort_order: int = pymongo.DESCENDING,
                  skip: conint(ge=0) = 0,
                  limit: conint(ge=5, multiple_of=5) = 10
                  ):

        todos = self.database[MONGO_COLLECTION_TODOS] \
            .find({}) \
            .sort([(sort_field, sort_order)]) \
            .skip(skip).limit(limit)
        total = self.database[MONGO_COLLECTION_TODOS].count_documents(filter={})

        return [ToDoItemInDB(**todo) for todo in todos], total

    def create_todo(self, todo: ToDoItemInDB) -> ToDoItemInDB:
        todo_in_db = jsonable_encoder(todo)
        new_todo = self.database[MONGO_COLLECTION_TODOS] \
            .insert_one(document=todo_in_db)
        created_todo = self.database[MONGO_COLLECTION_TODOS].find_one(
            {"_id": new_todo.inserted_id}
        )
        return ToDoItemInDB(**created_todo)
