import datetime
from typing import Union

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select

from models import tb_user
from scheams import User, UserInDB

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(db, username: str):
    stmt = select(tb_user).where(
        tb_user.c.username == username
    )
    result = await db.execute(stmt)
    result = result.fetchone()
    return result


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Union[datetime.timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(db, username: str, password: str):
    user = await get_user(db, username)
    print(user)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user
