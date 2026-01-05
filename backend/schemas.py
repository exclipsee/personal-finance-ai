from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# slight alias to vary style
StrOpt = Optional[str]


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
    description: StrOpt
    amount: float
    category: StrOpt


class TransactionOut(BaseModel):
    id: int
    date: Optional[date]
    description: StrOpt
    amount: float
    category: StrOpt

    class Config:
        orm_mode = True
