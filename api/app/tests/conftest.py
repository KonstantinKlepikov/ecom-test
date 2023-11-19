import pytest
from typing import Generator
from pydantic_settings import BaseSettings
from pydantic import MongoDsn
from pydantic_extra_types.phone_numbers import PhoneNumber
from pymongo import ASCENDING
from pymongo.client_session import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient
from app.main import app
from app.config import settings
from app.schemas.constraint import Collections
from app.db.init_db import get_session
from app.schemas.scheme_templates import Template


class TestSettings(BaseSettings):
    """Test settings"""
    TEST_MONGODB_URL: MongoDsn | None = None


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
def mock_data() -> tuple[dict[str, str], Template]:
    """Mock template data
    """
    m = {
        "name": "some template",
        "some_email": "some@email.com",
        "some_phone": "+7 000 000 00 00",
        "some_date": "2012.12.01",
        "some_text": "some text",
            }
    m_t = Template(
        name=m['name'],
        email=m['some_email'],
        phone=m['some_phone'],
        date=m['some_date'],
        text=m['some_text']
            )
    return m, m_t


@pytest.fixture(scope="function")
async def db() -> Generator:
    """Get mock mongodb
    """
    async with BdTestContext(
        test_settings.TEST_MONGODB_URL.unicode_string(),
        settings.DB_NAME
            ) as d:

        for collection in Collections.get_values():
            await d.create_collection(collection)
            if collection == Collections.TEMPLATES.value:
                await d[settings.DB_NAME][collection].create_index(
                    [('name', ASCENDING), ], unique=True
                        )
        yield d


@pytest.fixture(scope="function")
async def client(db) -> Generator:

    bd_test_client = AsyncIOMotorClient(
        test_settings.TEST_MONGODB_URL.unicode_string()
            )

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
