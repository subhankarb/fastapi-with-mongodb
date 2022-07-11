from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies.dependency_todo import get_todo_list, create_todo
from app.schemas.schema_request import ListToDoResponse, CreateToDoResponse

router = APIRouter()


@router.get(
    '/list.todos',
    status_code=HTTP_200_OK,
    name="todo:list",
    response_description="list todos",
    response_model=ListToDoResponse,
    response_model_exclude_none=True
)
def get_todo_list_api(
    todos: ListToDoResponse = Depends(get_todo_list)
):
    return todos


@router.post(
    '/todo.create',
    status_code=HTTP_200_OK,
    response_description="list todos",
    name="todo:create",
    response_model_exclude_none=True,
    response_model=CreateToDoResponse,
)
def create_todo_api(
    todo: CreateToDoResponse = Depends(create_todo)
):
    return todo
