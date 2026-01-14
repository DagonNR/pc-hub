from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_type = Column(String(), default="other", nullable=False, index=True)
    brand = Column(String(), nullable=False, index=True)
    model = Column(String(), nullable=False)
    notes = Column(String(), nullable=True)
    created_at = Column(DateTime(), default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    tickets = relationship("Ticket", back_populates="device")