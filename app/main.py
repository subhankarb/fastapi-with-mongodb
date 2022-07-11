import os
import json
import time
import traceback

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.core.core_config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME, VERSION, DEPLOYMENT_ENV
from app.core.core_events import create_start_app_handler, create_stop_app_handler
from app.resources import strings


def get_application() -> FastAPI:
    if DEPLOYMENT_ENV == "kube":
        prefix = os.environ.get('PROXY_PREFIX', '/')
        logger.info(f"DEPLOYMENT_ENV is {DEPLOYMENT_ENV} and proxy prefix {prefix}")
        application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION, openapi_prefix=prefix)
    else:
        application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(api_router)

    @application.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        try:
            start_time = time.time()
            response = await call_next(request)
            process_time = round(round((time.time() - start_time) * 1000, 2))
            response.headers["X-Process-Time"] = str(process_time) + " ms"
            logger.info("{0} took time {1} ms", request.url.path, process_time)
            return response
        except Exception:
            logger.error(traceback.print_exc())
            return Response(
                json.dumps(
                    {"loc": [], "msg": strings.INTERNAL_SERVER_ERROR, "type": "unexpected_error"}
                ),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = get_application()
