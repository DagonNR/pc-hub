from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.ticket import TicketOut, TicketCreate, TicketUpdate
from sqlalchemy.orm import Session
from app.core.deps import get_database
from app.models.ticket import Ticket
from typing import List

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/", response_model=List[TicketOut])
def list_tickets(db: Session = Depends(get_database)):
    tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    return tickets

@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_database)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

@router.post("/", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_database)):
    ticket = Ticket(
        device_id = payload.device_id,
        title = payload.title,
        description = payload.description,
        status = "new",
        priority = payload.priority.value,
        service_type = payload.service_type.value,
        estimated_cost = payload.estimated_cost,
        final_cost = None
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(payload: TicketUpdate, ticket_id: int, db: Session = Depends(get_database)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    data = payload.model_dump(exclude_unset=True)

    if "status" in data and data["status"] is not None:
        data["status"] = data["status"].value
    if "priority" in data and data["priority"] is not None:
        data["priority"] = data["priority"].value
    if "service_type" in data and data["service_type"] is not None:
        data["service_type"] = data["service_type"].value

    for key, value in data.items():
        setattr(ticket, key, value)
    
    db.commit()
    db.refresh(ticket)
    return ticket

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_database)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    db.delete(ticket)
    db.commit()
    return None