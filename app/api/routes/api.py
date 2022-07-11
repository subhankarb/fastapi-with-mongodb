from fastapi import APIRouter, Request

from app.api.routes import todo_routes, category_routes

router = APIRouter()

router.include_router(todo_routes.router, tags=["TODO V1"], prefix="/v1")
router.include_router(category_routes.router, tags=["CATEGORY V1"], prefix="/v1")


@router.get(
    "/v1/hello",
    name="probe:liveness"
)
def hello_world(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}