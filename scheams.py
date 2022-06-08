from pydantic import BaseModel, Field, validator
from typing import Union


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class RegisterModel(BaseModel):
    username: str = Field(..., max_length=10)
    password: str = Field(..., regex='', max_length=12, min_length=6)

    @validator('username')
    def username_must_be_that(cls, val):
        
        return val