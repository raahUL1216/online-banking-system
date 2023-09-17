from sqlalchemy import Column, ForeignKey, Integer, BigInteger, JSON, DateTime
from sqlalchemy.sql import func
from server.database import Base, engine

class MonthlyStatement(Base):
    __tablename__ = "statements"

    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    month = Column(Integer, nullable=False, primary_key=True)
    year = Column(Integer, nullable=False, primary_key=True)
    statement = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())


Base.metadata.create_all(engine)