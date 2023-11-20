from pymongo.client_session import ClientSession
from app.crud.crud_template import CRUDTemplate
from app.schemas.scheme_templates import Template, TemplateFields


class TestCRUDTemplates:

    async def test_get_many_return_template_from_db(
        self,
        db: ClientSession,
        crud_templates: CRUDTemplate,
        mock_data: tuple[dict[str, str], Template]
            ) -> None:
        """Test create many for templates
        """
        db_scheme = TemplateFields(**mock_data[1].model_dump())
        in_db = await crud_templates.get_many(db, db_scheme)
        assert isinstance(in_db, list), 'wrong type'
        assert len(in_db) == 1, 'wrong len'
        assert in_db[0]['name'] == mock_data[1].name, 'wrong data in db'
