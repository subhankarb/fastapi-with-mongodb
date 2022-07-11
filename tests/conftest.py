import asyncio
import warnings

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient


@pytest.yield_fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="class")
def app() -> FastAPI:
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from app.main import get_application

    return get_application()


@pytest.fixture(scope="class")
def http_test_client(app: FastAPI) -> TestClient:
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    client = TestClient(app)
    return client
