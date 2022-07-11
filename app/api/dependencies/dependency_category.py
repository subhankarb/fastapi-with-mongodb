from datetime import datetime
from typing import Literal, Optional

import pymongo
from fastapi import Depends, Body
from pydantic import conint

from app.api.dependencies.database import get_mongodb_repo
from app.db.repositories.category_repository import CategoryRepository
from app.schemas.schema_db import ToDoCategoryInDB
from app.schemas.schema_request import ListCategoryResponse, CreateCategoryResponse, CreateCategoryRequest


def get_category_list(
        sort: Literal["created_at_asc", "created_at_desc", "name_asc", "name_desc"] = None,
        page: Optional[conint(ge=1)] = 1,
        limit: conint(ge=5, multiple_of=5) = 10,
        category_repo: CategoryRepository = Depends(get_mongodb_repo(CategoryRepository))
) -> ListCategoryResponse:
    sort_field, sort_order = 'created_at', pymongo.DESCENDING
    if sort == "created_at_desc":
        sort_field, sort_order = 'created_at', pymongo.DESCENDING
    elif sort == "created_at_asc":
        sort_field, sort_order = 'created_at', pymongo.ASCENDING

    category_list_db, total = category_repo.list_categories(sort_field=sort_field,
                                                            sort_order=sort_order,
                                                            skip=(page - 1) * limit,
                                                            limit=limit)

    return ListCategoryResponse(categories=[
        CreateCategoryResponse(category_name=category_in_db.category_name,
                               category_id=str(category_in_db.id),
                               created_at=category_in_db.created_at)
        for category_in_db in category_list_db
    ],
        meta={
            'page': page,
            'limit': limit,
            'total': total
        })


def create_category(
        create_todo_req: CreateCategoryRequest = Body(..., ),
        category_repo: CategoryRepository = Depends(get_mongodb_repo(CategoryRepository))
) -> CreateCategoryResponse:
    category_in_db = ToDoCategoryInDB(category_name=create_todo_req.category_name,
                                      created_at=datetime.utcnow())
    category_created = category_repo.create_category(category_in_db)
    return CreateCategoryResponse(category_name=category_created.category_name,
                                  category_id=str(category_created.id),
                                  created_at=category_created.created_at)
