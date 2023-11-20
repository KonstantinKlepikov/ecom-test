from typing import TypeVar, Generic, Type, Any
from pydantic import BaseModel
from pymongo.client_session import ClientSession
from app.config import settings


SchemaDbType = TypeVar("SchemaDbType", bound=BaseModel)
SchemaReturnType = TypeVar("SchemaReturnType", bound=BaseModel)


class CRUDBase(Generic[SchemaDbType]):
    def __init__(
        self,
        schema: Type[SchemaReturnType],
        col_name: str,
        db_name: str = settings.DB_NAME
            ):
        """
        CRUD object with default methods to Create,
        Read, Update, Delete (CRUD).
        """
        self.schema = schema
        self.col_name = col_name
        self.db_name = db_name

    async def get_many(
        self,
        db: ClientSession,
        q: SchemaDbType,
        lenght: int = 100,
            ) -> list[dict[str, Any]]:
        """Get many documents

        Args:
            db (ClientSession): session
            q: (TemplateFields): query filter
            lenght (int, optional): maximum in result. Defaults to 100.

        Returns:
            list[dict[str, Any]]: search result
        """
        data = db.client[self.db_name][self.col_name].find(q.model_dump())
        return await data.to_list(length=lenght)
