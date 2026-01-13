from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(), nullable=False)
    category = Column(String(), default="other", nullable=False, index=True)
    brand = Column(String(), nullable=True, index=True)
    description = Column(String(), nullable=True)
    location  = Column(String(), nullable=True)
    stock  = Column(Integer(), nullable=False, index=True)
    unit_cost = Column(Numeric(10, 2), nullable=True,)
    unit_price = Column(Numeric(10, 2), nullable=True,)
    created_at = Column(DateTime(), default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    
    inventory_movements = relationship("InventoryMovement", back_populates="inventories")