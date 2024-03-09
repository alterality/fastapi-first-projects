from sqlalchemy import Table, Column, Integer, String, MetaData
from pydantic import BaseModel, EmailStr
from database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String, unique=True, index=True),
    Column("hashed_password", String),
)

class UserCreate(BaseModel):
    email: EmailStr
    password: str