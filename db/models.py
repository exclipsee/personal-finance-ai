from sqlalchemy import Column, Integer, String, Date, Float, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Col = Column

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Col(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=True, index=True)
    description = Column(String(512), nullable=True)
    amount = Column(Float, nullable=False)
    category = Column(String(128), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    user = relationship('User', back_populates='transactions')


class User(Base):
    __tablename__ = 'users'

    id = Col(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    email = Column(String(320), unique=True, nullable=True, index=True)
    hashed_password = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship('Transaction', back_populates='user')


class CategoryFeedback(Base):
    __tablename__ = 'category_feedback'

    id = Col(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    old_category = Column(String(128), nullable=True)
    new_category = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

