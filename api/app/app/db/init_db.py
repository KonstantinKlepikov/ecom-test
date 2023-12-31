from typing import Generator
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from pymongo.client_session import ClientSession
from pymongo.errors import CollectionInvalid
from fastapi.logger import logger as fastAPI_logger
from app.config import settings
from app.schemas.constraint import Collections


def get_client(mongodb_url: str) -> AsyncIOMotorClient:
    """Get mongo db

    Args:
        mongodb_url (str): url to mongo

    Returns:
        AsyncIOMotorClient: client exemplar
    """
    fastAPI_logger.info("Create mongo client")
    return AsyncIOMotorClient(mongodb_url)


client = get_client(settings.MONGODB_URL.get_secret_value())


async def create_collections() -> None:  #
    """Create collections
    """
    for collection in Collections.get_values():
        try:
            await client[settings.DB_NAME].create_collection(collection)
            if collection == Collections.TEMPLATES.value:
                await client[settings.DB_NAME][collection].create_index(
                    [('name', ASCENDING), ], unique=True
                        )
        except CollectionInvalid:
            continue


async def get_session() -> Generator[ClientSession, None, None]:
    """Get mongo session
    """
    try:
        fastAPI_logger.info("Create mongo session")
        session = await client.start_session()
        yield session
    finally:
        await session.end_session()
