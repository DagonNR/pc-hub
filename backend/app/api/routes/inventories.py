from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.inventory import InventoryOut, InventoryCreate, InventoryUpdate
from sqlalchemy.orm import Session
from app.core.deps import get_database
from app.models.inventory import Inventory
from typing import List

router = APIRouter(prefix="/inventories", tags=["inventory"])

@router.get("/", response_model=List[InventoryOut])
def list_inventory(db: Session = Depends(get_database)):
    inventories = db.query(Inventory).order_by(Inventory.created_at.desc()).all()
    return inventories

@router.get("/{inventory_id}", response_model=InventoryOut)
def get_inventory(inventory_id: int, db: Session = Depends(get_database)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return inventory

@router.post("/", response_model=InventoryOut, status_code=status.HTTP_201_CREATED)
def create_inventory(payload: InventoryCreate, db: Session = Depends(get_database)):
    inventory = Inventory(
        name = payload.name,
        category = payload.category.value,
        brand = payload.brand,
        description = payload.description,
        location = payload.location,
        stock = payload.stock,
        unit_cost = payload.unit_cost,
        unit_price = payload.unit_price
    )
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

@router.patch("/{inventory_id}", response_model=InventoryOut)
def update_inventory(payload: InventoryUpdate, inventory_id: int, db: Session = Depends(get_database)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    data = payload.model_dump(exclude_unset=True)

    if "category" in data and data["category"] is not None:
        data["category"] = data["category"].value

    for key, value in data.items():
        setattr(inventory, key, value)
    
    db.commit()
    db.refresh(inventory)
    return inventory

@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(inventory_id: int, db: Session = Depends(get_database)):
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(inventory)
    db.commit()
    return None