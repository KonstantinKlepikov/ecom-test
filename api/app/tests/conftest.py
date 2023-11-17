import pytest
from typing import Generator
from pydantic_settings import BaseSettings
from pydantic import SecretStr
from pymongo import ASCENDING
from pymongo.client_session import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient
from app.main import app
from app.schemas.constraint import Collections
from app.db.init_db import get_session


class TestSettings(BaseSettings):
    """Test settings"""
    TEST_MONGO_DB: str | None = None
    TEST_MONGODB_URL: SecretStr | None = None


test_settings = TestSettings()


class BdTestContext:
    def __init__(self, mongodb_url: str, db_name: str):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db_name = db_name

    async def __aenter__(self):
        return self.client[self.db_name]

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.drop_database(self.db_name)
        self.client.close()


@pytest.fixture(scope="function")
async def db() -> Generator:
    """Get mock mongodb
    """
    async with BdTestContext(
        test_settings.TEST_MONGODB_URL,
        test_settings.TEST_MONGO_DB
            ) as d:

        for collection in Collections.get_values():
            await d.create_collection(collection)
            if collection == Collections.TEMPLATES.value:
                await d[test_settings.TEST_MONGO_DB][collection].create_index(
                    [('name', ASCENDING), ], unique=True
                        )
        yield d


@pytest.fixture(scope="function")
async def client(db) -> Generator:

    bd_test_client = AsyncIOMotorClient(test_settings.TEST_MONGODB_URL)

    async def mock_session() -> Generator[ClientSession, None, None]:
        """Get mongo session
        """
        try:
            session = await bd_test_client.start_session()
            yield session
        finally:
            await session.end_session()

    app.dependency_overrides[get_session] = mock_session

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

    app.dependency_overrides = {}
    bd_test_client.close()
