from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer(), ForeignKey("devices.id"), index=True, nullable=True)
    client_id = Column(Integer(), ForeignKey("clients.id"), index=True, nullable=False)
    title = Column(String(), nullable=False)
    description = Column(String(), nullable=True)
    status = Column(String(), default="new", nullable=False, index=True)
    priority = Column(String(), default="medium", nullable=False, index=True)
    service_type = Column(String(), default="repair", nullable=False, index=True)
    estimated_cost = Column(Numeric(precision=10, scale=2), nullable=True)
    final_cost = Column(Numeric(precision=10, scale=2), nullable=True)
    created_at = Column(DateTime(), default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    device = relationship("Device", back_populates="tickets")
    inventory_movements = relationship("InventoryMovement", back_populates="tickets")
    client = relationship("Client", back_populates="tickets")