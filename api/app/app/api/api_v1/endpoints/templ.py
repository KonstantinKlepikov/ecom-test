from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Query, Request
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from app.db.init_db import get_session
from app.schemas.scheme_templates import TemplateName, RequestTyped
from app.config import settings
from app.crud.crud_template import templates


router = APIRouter()


@router.post(
    "/get_form",
    status_code=status.HTTP_200_OK,
    summary='Get template by template pattern',
    response_description="Ok.",
    response_model=TemplateName | RequestTyped,
    responses=settings.ERRORS
        )
async def get_form(
    request: Request,
    db: ClientSession = Depends(get_session)
        ) -> TemplateName | RequestTyped:
    """Get template by template_name

    NOTE: хочется обратить внимание, что использование
    ресукрса с именем get_ в POST-запросе это святотатство :)
    """
    params = request.query_params._dict
    # TODO: here we validate each fields by value type,
    # and use only fields existed in templates db. As result we create
    # object like: field_name: field tipe

    # TODO: raise if existed fields less than 4 or multiple with same type

    # TODO: search db. If exist -> name. if not -> field types
    return TemplateName(**params)
