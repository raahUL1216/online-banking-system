from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func

from app.database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement='auto')
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())

Base.metadata.create_all(engine)
