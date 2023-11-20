from app.config import settings
from app.crud.crud_base import CRUDBase
from app.schemas.scheme_templates import Template, TemplateFields
from app.schemas.constraint import Collections


class CRUDTemplate(CRUDBase[TemplateFields]):
    """Templates crud
    """


templates = CRUDTemplate(
    schema=Template,
    col_name=Collections.TEMPLATES.value,
    db_name=settings.DB_NAME,
        )
