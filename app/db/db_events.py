from fastapi import FastAPI
from loguru import logger
from pymongo import MongoClient

from app.core.core_config import (
    MONGODB_URL, MONGODB_MAX_CONNECTIONS_COUNT, MONGODB_MIN_CONNECTIONS_COUNT,
)


class MongoDB:
    client: MongoClient = None


mongo_db = MongoDB()


def connect_to_mongo(app: FastAPI) -> None:
    logger.info("Connect to the Mongodb...")
    mongo_client = MongoClient(
        MONGODB_URL,
        maxPoolSize=MONGODB_MAX_CONNECTIONS_COUNT,
        minPoolSize=MONGODB_MIN_CONNECTIONS_COUNT,
    )
    mongo_db.client = mongo_client
    app.state.mongo_client = mongo_client
    logger.info("Mongodb connection succeeded！")


def close_mongo_connection(app: FastAPI) -> None:
    logger.info("Closing the mongodb connection..")
    app.state.mongo_client.close()
    logger.info("Mongodb connection closed！")
