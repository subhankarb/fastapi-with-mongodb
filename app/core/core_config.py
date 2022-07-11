import logging
import sys
import os
from typing import List
from pathlib import Path

from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

from app.core.core_logging import Formatter, InterceptHandler

VERSION = "0.0.1"
ROOT_PATH = Path(__file__).parent.parent.parent
env_file = os.environ.get("ENV_FILE") if "ENV_FILE" in os.environ else os.path.join(ROOT_PATH, ".env")

config = Config(env_file)

# ======= DATABASE ==========

MONGODB_URL: str = config("MONGODB_URL", default="mongodb://dbuser:dbpass@127.0.0.1:27017/")
MONGO_DATABASE: str = config("MONGO_DATABASE", default="test")
MONGODB_MAX_CONNECTIONS_COUNT: int = config("MONGODB_MAX_CONNECTIONS_COUNT", cast=int, default=20)
MONGODB_MIN_CONNECTIONS_COUNT: int = config("MONGODB_MIN_CONNECTIONS_COUNT", cast=int, default=1)

MONGO_COLLECTION_TODOS: str = config("MONGO_COLLECTION_TODOS", default="todos")
MONGO_COLLECTION_CATEGORIES: str = config("MONGO_COLLECTION_CATEGORIES", default="categories")

# =========== PROJECT ==========
PROJECT_NAME: str = config("PROJECT_NAME", default="Waterdip")
DEBUG: bool = config("DEBUG", cast=bool, default=False)
UNIT_TEST = config("UNIT_TEST", cast=bool, default=False)
DEPLOYMENT_ENV: str = config("DEPLOYMENT_ENV", default="local")
ALLOWED_HOSTS: List[str] = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="*")
AIO_CLIENT_TOUT_SEC: int = config("AIO_CLIENT_TOUT_SEC", cast=int, default=10)


# =========== LOGGING ==========
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL)
logger.configure(
    handlers=[{"sink": sys.stdout, "level": LOGGING_LEVEL, "format": Formatter().format}]
)
