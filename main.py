from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.sql import select
from database import database, engine, metadata
from models import users
from auth import create_access_token, verify_password, get_password_hash
from schemas import UserCreate, Token

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(bind=engine)  # Эта строка должна быть здесь, чтобы гарантировать создание таблиц при запуске приложения.

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/register/", response_model=Token)
async def register_user(user: UserCreate = Depends()):
    query = select(users).where(users.c.email == user.email)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    query = users.insert().values(email=user.email, hashed_password=hashed_password)
    await database.execute(query)
    return {"access_token": create_access_token(data={"sub": user.email}), "token_type": "bearer"}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_query = select([users]).where(users.c.email == form_data.username)
    user = await database.fetch_one(user_query)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Возвращение токена для аутентифицированного пользователя
    return {"access_token": create_access_token(data={"sub": user.email}), "token_type": "bearer"}
