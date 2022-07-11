import time
from typing import Any, Tuple

from loguru import logger
from pymongo import MongoClient

from app.core.core_config import MONGO_DATABASE


def _log_query(query: str, query_params: Tuple[Any, ...]) -> None:
    logger.debug("query: {0}, values: {1}", query, query_params)


class PyMongoBaseRepo:

    def __init__(self, mongo: MongoClient):
        self._mongo = mongo
        self.database = self._mongo[MONGO_DATABASE]

    @property
    def mongo_client(self) -> MongoClient:
        return self._mongo
