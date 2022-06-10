from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from models import tb_user
from scheams import User, TokenData, UserInDB
from utils import SECRET_KEY, ALGORITHM, verify_password, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


engine = create_async_engine(
    'mysql+aiomysql://root:123456@mysql/siwen?charset=utf8mb4',
    echo=True,
    pool_size=5,
    pool_recycle=120,
    max_overflow=5
    # json_deserializer=ujson.loads,
    # json_serializer=ujson.dumps,
)


async def get_db():
    async with engine.connect() as conn:
        yield conn


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
