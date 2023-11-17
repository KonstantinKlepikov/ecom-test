from typing_extensions import Annotated
from pydantic import BaseModel, constr, validator
from pydantic.functional_validators import AfterValidator
from bson.objectid import ObjectId
from app.schemas.constraint import FieldTypes


class TemplateName(BaseModel):
    """Template name
    """
    name: str

    class Config:

        json_schema_extra = {
                "example": {
                    "name": "some_name_field_name",
                        }
                    }



class Template(TemplateName):
    """Template
    """
    email: str
    phone: str
    date: str
    text: str

    class Config:

        json_schema_extra = {
                "example": {
                    "name": "some_name_field_name",
                    "email": "some_email_field_name",
                    "phone": "some_phone_field_name",
                    "date": "some_date_field_name",
                    "text": "some_text_field_name",
                        }
                    }


class RequestScheme(BaseModel):
    """Request data
    """

    class Config:

        json_schema_extra = {
                "example": {
                        }
                    }


class RequestTyped(BaseModel):
    """Typed request
    """

    class Config:

        json_schema_extra = {
                "example": {
                        }
                    }
