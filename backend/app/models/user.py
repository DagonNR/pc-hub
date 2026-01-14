from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.schemas.user import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.client, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    client = relationship("Client", back_populates="user", uselist=False, single_parent=True)