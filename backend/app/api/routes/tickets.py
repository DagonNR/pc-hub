from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.ticket import TicketOut, TicketCreate, TicketUpdate
from app.schemas.user import UserRole
from sqlalchemy.orm import Session
from app.core.deps import get_database, require_roles, get_current_user
from app.models.ticket import Ticket
from app.models.client import Client
from app.models.device import Device
from app.models.user import User
from typing import List

router = APIRouter(prefix="/tickets", tags=["tickets"], dependencies=[Depends(require_roles(UserRole.admin, UserRole.tech, UserRole.client))])

@router.get("/", response_model=List[TicketOut])
def list_tickets(db: Session = Depends(get_database), current_user: User = Depends(get_current_user) ):
    #tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    #return tickets
    q = db.query(Ticket).order_by(Ticket.created_at.desc())

    if current_user.role in (UserRole.admin, UserRole.tech):
        return q.all()
    
    return q.join(Client).filter(Client.user_id == current_user.id).all()


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_database), current_user = Depends(require_roles(UserRole.admin, UserRole.tech))):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket

@router.post("/", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_database), current_user = Depends(require_roles(UserRole.admin, UserRole.tech))):
    if payload.estimated_cost <= 0:
        raise HTTPException(400, "Número invalido")
    
    client = db.query(Client).filter(Client.id == payload.client_id).first()
    if not client:
        raise HTTPException(404, "Cliente no encontrado")

    if payload.device_id is not None:
        device = db.query(Device).filter(Device.id == payload.device_id).first()
        if not device:
            raise HTTPException(404, "Dispositivo no encontrado")

    ticket = Ticket(
        device_id = payload.device_id,
        client_id = payload.client_id,
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
def update_ticket(payload: TicketUpdate, ticket_id: int, db: Session = Depends(get_database), current_user = Depends(require_roles(UserRole.admin))):
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
def delete_ticket(ticket_id: int, db: Session = Depends(get_database), current_user = Depends(require_roles(UserRole.admin))):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    db.delete(ticket)
    db.commit()
    return None