
from sqlalchemy import Column, BigInteger, String
from app.db.database import Base


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(BigInteger, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False)
