import datetime
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert

from models import tb_user
from scheams import User, UserInDB, RegisterIn
from depends import oauth2_scheme, get_current_active_user, get_db
from utils import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context

app = FastAPI()


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    print('---', form_data.username, form_data.password)
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register")
async def register(body: RegisterIn, db=Depends(get_db)):
    # 判断用户名是否存在
    stmt_query = select(tb_user).where(
        tb_user.c.username == body.username
    )
    result = await db.execute(stmt_query)
    result = result.fetchone()
    if result:
        print('用户名已存在', body.username)
        return {'errcode': '', 'errmsg': '用户名已存在:%s' % body.username}
    # 否则向数据库写入用户

    stmt_insert = insert(tb_user).values(
        username=body.username,
        password=pwd_context.hash(body.password),
        create_time=datetime.datetime.utcnow()
    )
    await db.execute(stmt_insert)
    await db.commit()
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": body.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
