
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True)
    role_id = Column(
        BigInteger,
        ForeignKey("roles.role_id"),
        nullable=False
    )
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True))
