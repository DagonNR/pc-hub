from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime 

class Client(Base):
    __tablename__= "clients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer(), ForeignKey("users.id"), index=True, nullable=False, unique=True)
    first_name = Column(String(), nullable=False, index=True)
    last_name = Column(String(), nullable=False, index=True)
    rfc = Column(String(13), nullable=False, index=True)
    email = Column(String(), nullable=False, index=True)
    phone_number = Column(String(10), nullable=True)
    street_adress = Column(String(), nullable=False)
    interior_number = Column(String(6), nullable=True)
    outer_number = Column(String(6), nullable=False)
    postal_code = Column(String(5), nullable=False)
    city = Column(String(), nullable=False)
    state = Column(String(), nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow, nullable=False, index=True)
    update_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tickets = relationship("Ticket", back_populates="client")
    user = relationship("User", back_populates="client")
