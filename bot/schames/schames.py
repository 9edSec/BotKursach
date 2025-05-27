from pydantic import BaseModel, field_validator

from bot.schames.validators import validator_one_of_tuple

class RegUserType(BaseModel):
    user_type: str

    @field_validator('user_type', mode='after')
    @classmethod
    def valid_user_type(cls, value):
        validator_one_of_tuple(value)
