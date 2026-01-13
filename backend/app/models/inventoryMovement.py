from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class InventoryMovement(Base):
    __tablename__ = "inventory_movement"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer(), ForeignKey("inventory.id"), index=True, nullable=True)
    ticket_id = Column(Integer(), ForeignKey("tickets.id"), index=True, nullable=True)
    movement_type = Column(String(), default="inside", nullable=False, index=True)
    adjustment_direction = Column(String(), default="increase", index=True, nullable=True)
    quantity = Column(Integer(), nullable=False)
    reason = Column(String(), default="purchase", nullable=False, index=True)
    description = Column(String(), nullable=True)
    unit_cost = Column(Numeric(10, 2), nullable=True,)
    unit_price = Column(Numeric(10, 2), nullable=True,)
    created_at = Column(DateTime(), default=datetime.utcnow, nullable=False, index=True)

    inventories = relationship("Inventory", back_populates="inventory_movements")
    tickets = relationship("Ticket", back_populates="inventory_movements")