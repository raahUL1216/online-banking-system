from sqlalchemy import Column, ForeignKey, BigInteger, Float, String, DateTime
from sqlalchemy.sql import func
from server.database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement='auto')
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())

class UserAccount(Base):
    __tablename__ = "user_account"

    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    balance = Column(Float, default=0)
    updated_at = Column(DateTime(timezone=False), server_default=func.now())


Base.metadata.create_all(engine)