from typing import Any
from pydantic import BaseModel, model_validator
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from email_validator import validate_email, EmailNotValidError
from dateutil.parser import parser, ParserError
from pydantic_core import PydanticCustomError
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


class TemplateFields(BaseModel):
    """Template withou text field
    """
    email: str
    phone: str
    date: str

    class Config:

        json_schema_extra = {
                "example": {
                    "email": "some_email_field_name",
                    "phone": "some_phone_field_name",
                    "date": "some_date_field_name",
                    "text": "some_text_field_name",
                        }
                    }


class Template(TemplateName, TemplateFields):
    """Template
    """
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


class FindedTemplateNames(BaseModel):
    """Finded in db names of templates
    """
    finded_names: list[TemplateName] = []

    class Config:

        json_schema_extra = {
                "example": {
                    "finded_names": ["some_name_field_name", ],
                        }
                    }


class RequestScheme(BaseModel):
    """Request data validation
    """

    class Config:
        extra='allow'

    @model_validator(mode='before')
    @classmethod
    def validate_all(cls, data: dict) -> Any:
        """Validate all fields
        """
        result = {
            'email': None,
            'phone': None,
            'date': None,
            'text_fields': []
                }
        for k,v in data.items():

            # validate email
            try:
                validate_email(v, check_deliverability=False)
                if result['email'] is None:
                    result['email'] = k
                    continue
                else:
                    raise PydanticCustomError(
                        'Wrong request data',
                        'To many emails in request data'
                            )
            except EmailNotValidError:
                pass

            # validate phone
            try:
                p = phonenumbers.parse(v, None)
                if phonenumbers.is_possible_number(p):
                    if result['phone'] is None:
                        result['phone'] = k
                        continue
                    else:
                        raise PydanticCustomError(
                            'Wrong request data',
                            'To many phone numbers in request data'
                                )
            except NumberParseException:
                pass

            # validate date
            try:
                parser().parse(v)
                if result['date'] is None:
                    result['date'] = k
                    continue
                else:
                    raise PydanticCustomError(
                        'Wrong request data',
                        "To many dates in request data"
                            )
            except (ParserError, OverflowError):
                pass

            # validate text
            if isinstance(v, str):
                result['text_fields'].append(k)


        # if no email, phone, date or text
        if all(result.values()) is not True:
            raise PydanticCustomError(
                'Wrong request data',
                'Not all 4 fields are exist in request data'
                    )

        return result


class RequestTyped(BaseModel):
    """Typed request
    """

    class Config:
        extra='allow'

    @model_validator(mode='before')
    @classmethod
    def validate_all(cls, data: dict) -> Any:
        """Validate all fields
        """
        data.update({name: 'text' for name in data['text_fields']})
        del data['text_fields']
        print(data)
        return data



