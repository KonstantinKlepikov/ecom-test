from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Query
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from app.db.init_db import get_session
from app.schemas.scheme_templates import Template, TypedRequestScheme
from app.config import settings
from app.crud.crud_template import templates


router = APIRouter()


@router.get(
    "/get",
    status_code=status.HTTP_200_OK,
    summary='Get template by template pattern',
    response_description="Ok.",
    response_model=Template,
    responses=settings.ERRORS
        )
async def get_template(
    db: ClientSession = Depends(get_session)
        ) -> Template | TypedRequestScheme:
    """Get template by template_name
    """
