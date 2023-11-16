from typing import Any
from pymongo.client_session import ClientSession
from app.config import settings
from app.crud.crud_base import CRUDBase
from app.schemas.scheme_templates import Template
from app.schemas.constraint import Collections


class CRUDTemplate(CRUDBase[Template]):
    """Templates crud
    """

templates = CRUDTemplate(
    schema=Template,
    col_name=Collections.TEMPLATES.value,
    db_name=settings.DB_NAME,
        )
