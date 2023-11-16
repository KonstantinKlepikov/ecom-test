from typing_extensions import Annotated
from pydantic import BaseModel, constr, validator
from pydantic.functional_validators import AfterValidator
from bson.objectid import ObjectId


class Template(BaseModel):
    """Template response
    """
    class Config:

        json_schema_extra = {
                "example": {
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


class TypedRequestScheme(BaseModel):
    """Typed request
    """

    class Config:

        json_schema_extra = {
                "example": {
                        }
                    }
