import pytest
from typing import Callable
from httpx import AsyncClient
from app.config import settings
from app.crud.crud_template import CRUDTemplate
from app.schemas.scheme_templates import Template


class TestTemplatesApi:

    # @pytest.fixture(scope="function")
    # async def mock_get(
    #     self,
    #     crud_template: CRUDTemplate,
    #     monkeypatch,
    #         ) -> Callable:
    #     """Mock template get
    #     """
    #     async def mock_return(*args, **kwargs) -> Callable:
    #         return await crud_template.get(args[0], args[1])
    #     monkeypatch.setattr(templates, "get", mock_return)

    async def test_templates_create_returns_200(
        self,
        client: AsyncClient,
        mock_data: tuple[dict[str, str], Template],
            ) -> None:
        """Test create template
        """
        response = await client.post(
            f"{settings.API_V1}/templates/get_form",
            params=mock_data[0],
                )
        assert response.status_code == 200, f'{response.content=}'
