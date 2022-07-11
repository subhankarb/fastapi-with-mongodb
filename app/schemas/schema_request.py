from datetime import datetime
from typing import List, Optional, Dict, Union

from pydantic import BaseModel

from app.schemas.schema_db import PyObjectId


class CreateCategoryRequest(BaseModel):
    category_name: str


class CreateCategoryResponse(BaseModel):
    category_name: str
    category_id: str
    created_at: datetime


class ListCategoryResponse(BaseModel):
    categories: List[CreateCategoryResponse]
    meta: Optional[Dict[str, Union[str, int]]]


class CreateToDoRequest(BaseModel):
    name: str
    description: Optional[str]
    category_id: str


class CreateToDoResponse(BaseModel):
    name: str
    description: Optional[str]
    category_id: str
    todo_id: str


class ListToDoResponse(BaseModel):
    todos: List[CreateToDoResponse]
    meta: Optional[Dict[str, Union[str, int]]]
