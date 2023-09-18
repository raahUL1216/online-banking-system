from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String, JSON, DateTime
from sqlalchemy.sql import func
from server.database import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement='auto')
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())


# composite primary key will be (user_id, month, year), but removed it as scheduler runs 10sec periodically for demonstration purpose (will give unique constraint error if this primary key is specified). 
class MonthlyStatement(Base):
    __tablename__ = "statements"

    id = Column(BigInteger, primary_key=True, autoincrement='auto')
    user_id = Column(BigInteger, ForeignKey('users.id'))
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    statement = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())


Base.metadata.create_all(engine)