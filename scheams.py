from pydantic import BaseModel, Field, validator
from typing import Union


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class RegisterIn(BaseModel):
    username: str = Field(..., min_length=6, max_length=12, regex='[a-zA-Z_][a-zA-Z0-9_]{5,11}')
    password: str = Field(..., min_length=6)
