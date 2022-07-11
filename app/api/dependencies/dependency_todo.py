from datetime import datetime
from typing import Literal, Optional

import pymongo
from fastapi import Depends, Body
from pydantic import conint

from app.api.dependencies.database import get_mongodb_repo
from app.db.repositories.todo_repository import TodoRepository
from app.schemas.schema_db import ToDoItemInDB, PyObjectId
from app.schemas.schema_request import ListToDoResponse, CreateToDoResponse, CreateToDoRequest


def get_todo_list(
        sort: Literal["created_at_asc", "created_at_desc", "name_asc", "name_desc"] = None,
        page: Optional[conint(ge=1)] = 1,
        limit: conint(ge=5, multiple_of=5) = 10,
        todo_repo: TodoRepository = Depends(get_mongodb_repo(TodoRepository))
) -> ListToDoResponse:
    sort_field, sort_order = 'created_at', pymongo.DESCENDING
    if sort == "created_at_desc":
        sort_field, sort_order = 'created_at', pymongo.DESCENDING
    elif sort == "created_at_asc":
        sort_field, sort_order = 'created_at', pymongo.ASCENDING

    todo_list_db, total = todo_repo.list_todo(sort_field=sort_field,
                                              sort_order=sort_order,
                                              skip=(page - 1) * limit,
                                              limit=limit)

    return ListToDoResponse(todos=[
        CreateToDoResponse(name=todo.name,
                           description=todo.description,
                           category_id=str(todo.category_id),
                           todo_id=str(todo.id)
                           )
        for todo in todo_list_db
    ],
            meta={
                'page': page,
                'limit': limit,
                'total': total
            })


def create_todo(
        create_todo_req: CreateToDoRequest = Body(..., ),
        todo_repo: TodoRepository = Depends(get_mongodb_repo(TodoRepository))
) -> CreateToDoResponse:
    todo_in_db = ToDoItemInDB(name=create_todo_req.name,
                              description=create_todo_req.description,
                              created_at=datetime.utcnow(),
                              category_id=PyObjectId(create_todo_req.category_id))
    todo_created = todo_repo.create_todo(todo_in_db)
    return CreateToDoResponse(todo_id=str(todo_created.id),
                              name=todo_created.name,
                              category_id=str(todo_created.category_id))
