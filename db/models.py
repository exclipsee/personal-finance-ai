from sqlalchemy import Column, Integer, String, Date, Float, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=True, index=True)
    description = Column(String(512), nullable=True)
    amount = Column(Float, nullable=False)
    category = Column(String(128), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
