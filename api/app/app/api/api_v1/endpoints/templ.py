from fastapi import APIRouter, status, Depends, HTTPException, Request
from pymongo.client_session import ClientSession
from pydantic_core import ValidationError
from app.db.init_db import get_session
from app.schemas.scheme_templates import (
    TemplateName,
    TemplateFields,
    RequestTyped,
    RequestScheme,
    FindedTemplateNames,
        )
from app.config import settings
from app.crud.crud_template import templates
from app.core.check import check_text


router = APIRouter()


@router.post(
    "/get_form",
    status_code=status.HTTP_200_OK,
    summary='Get template by template pattern',
    response_description="Ok.",
    responses=settings.ERRORS
        )
async def get_form(
    request: Request,
    db: ClientSession = Depends(get_session)
        ):
    """Get template by template_name

    NOTE: хочется обратить внимание, что использование
    ресурса с именем get_ в POST-запросе это святотатство :)

    К тому же, множественными схемами мы создаем
    ситуацию неопределенного контратка. FastAPI это не поддерживает.
    """
    params = request.query_params._dict

    try:
        request_scheme = RequestScheme(**params)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.json())

    db_scheme = TemplateFields(**request_scheme.model_dump())

    in_db = await templates.get_many(db, db_scheme)
    checked = check_text(in_db, request_scheme.text_fields)

    if checked:
        return FindedTemplateNames(
            finded_names=[TemplateName(**resp)for resp in checked]
                )
    else:
        return RequestTyped(**request_scheme.model_dump())
