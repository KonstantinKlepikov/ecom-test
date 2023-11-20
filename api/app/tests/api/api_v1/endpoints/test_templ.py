import pytest
from typing import Callable
from httpx import AsyncClient
from app.config import settings
from app.crud.crud_template import CRUDTemplate
from app.schemas.scheme_templates import Template
from app.crud.crud_template import templates


class TestTemplatesApi:

    @pytest.fixture(scope="function")
    async def mock_get_many(
        self,
        crud_template: CRUDTemplate,
        monkeypatch,
            ) -> Callable:
        """Mock template get
        """
        async def mock_return(*args, **kwargs) -> Callable:
            return await crud_template.get(args[0], args[1])
        monkeypatch.setattr(templates, "get_many", mock_return)

    async def test_templates_returns_200(
        self,
        client: AsyncClient,
        mock_data: tuple[dict[str, str], Template],
            ) -> None:
        """Test template
        """
        response = await client.post(
            f"{settings.API_V1}/templates/get_form",
            params=mock_data[0],
                )
        assert response.status_code == 200, f'{response.content=}'

    async def test_templates_raises_400(
        self,
        client: AsyncClient,
        mock_data: tuple[dict[str, str], Template],
            ) -> None:
        """Test template raises 400 if data not complete
        """
        del mock_data[0]['some_email']
        response = await client.post(
            f"{settings.API_V1}/templates/get_form",
            params=mock_data[0],
                )
        assert response.status_code == 400, f'{response.content=}'

    async def test_templates_returns_typed_data(
        self,
        client: AsyncClient,
        mock_data: tuple[dict[str, str], Template],
            ) -> None:
        """Test typed response content
        """
        mock_data[0]['additional_phone'] = "+7 900 000 00 00"
        del mock_data[0]["some_phone"]
        response = await client.post(
            f"{settings.API_V1}/templates/get_form",
            params=mock_data[0],
                )
        assert response.status_code == 200, f'{response.content=}'
