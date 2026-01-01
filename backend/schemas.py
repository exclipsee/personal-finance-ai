from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TransactionCreate(BaseModel):
    date: Optional[date]
    description: Optional[str]
    amount: float
    category: Optional[str]


class TransactionOut(BaseModel):
    id: int
    date: Optional[date]
    description: Optional[str]
    amount: float
    category: Optional[str]

    class Config:
        orm_mode = True
