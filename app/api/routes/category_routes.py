from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies.dependency_category import get_category_list, create_category
from app.api.dependencies.dependency_todo import get_todo_list, create_todo
from app.schemas.schema_request import ListToDoResponse, CreateToDoResponse, ListCategoryResponse, \
    CreateCategoryResponse

router = APIRouter()


@router.get(
    '/list.categories',
    status_code=HTTP_200_OK,
    name="category:list",
    response_description="list categories",
    response_model=ListCategoryResponse,
    response_model_exclude_none=True
)
def get_category_list_api(
    category_list_response: ListCategoryResponse = Depends(get_category_list)
):
    return category_list_response


@router.post(
    '/category.create',
    status_code=HTTP_200_OK,
    response_description="create category",
    name="category:create",
    response_model_exclude_none=True,
    response_model=CreateCategoryResponse,
)
def create_category_api(
    category_created: CreateCategoryResponse = Depends(create_category)
):
    return category_created
