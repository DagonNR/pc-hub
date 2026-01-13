from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_database
from app.models.client import Client
from app.schemas.client import ClientOut, ClientCreate, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/", response_model=List[ClientOut])
def list_clients(db: Session = Depends(get_database)):
    clients = db.query(Client).order_by(Client.created_at.desc()).all()
    return clients

@router.get("/{client_id}", response_model=ClientOut)
def get_client(client_id: int, db: Session = Depends(get_database)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@router.post("/", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate, db: Session = Depends(get_database)):
    client = Client(
        first_name=payload.first_name,
        last_name=payload.last_name,
        rfc=payload.rfc,
        email=payload.email,
        phone_number=payload.phone_number,
        street_adress=payload.street_adress,
        interior_number=payload.interior_number,
        outer_number=payload.outer_number,
        postal_code=payload.postal_code,
        city=payload.city,
        state=payload.state,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.patch("/{client_id}", response_model=ClientOut)
def update_client(payload: ClientUpdate, client_id: int, db: Session = Depends(get_database)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    data = payload.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_database)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db.delete(client)
    db.commit()
    return None
