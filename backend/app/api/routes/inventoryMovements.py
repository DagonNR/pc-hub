from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.inventoryMovement import InventoryMovementOut, InventoryMovementCreate
from sqlalchemy.orm import Session
from app.core.deps import get_database
from app.models.inventoryMovement import InventoryMovement
from typing import List
from app.models.inventory import Inventory

router = APIRouter(prefix="/inventoryMovements", tags=["inventoryMovements"])

@router.get("/", response_model=List[InventoryMovementOut])
def list_inventory_movements(db: Session = Depends(get_database)):
    inventoryMovements = db.query(InventoryMovement).order_by(InventoryMovement.created_at.desc()).all()
    return inventoryMovements

@router.get("/{inventory_movement_id}", response_model=InventoryMovementOut)
def get_inventory_movement(inventory_movement_id: int, db: Session = Depends(get_database)):
    inventoryMovement = db.query(InventoryMovement).filter(InventoryMovement.id == inventory_movement_id).first()
    if not inventoryMovement:
        raise HTTPException(status_code=404, detail="Movimiento de inventario no encontrado")
    return inventoryMovement

@router.post("/", response_model=InventoryMovementOut, status_code=status.HTTP_201_CREATED)
def create_inventory_movement(payload: InventoryMovementCreate, db: Session = Depends(get_database)):

    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

    inventory = db.query(Inventory).filter(Inventory.id == payload.inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Producto de inventario no encotrado")

    m_type = payload.movement_type.value

    if m_type == "out":
        if inventory.stock < payload.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Producto sin stock. Stock acutal={inventory.stock}, Petición de={payload.quantity}"
            )
        inventory.stock -= payload.quantity

    elif m_type == "inside":
        inventory.stock += payload.quantity

    elif m_type == "adjustment":
        if payload.adjustment_direction is None:
            raise HTTPException(status_code=400, detail="Favor de llenar el campo adjustment_direction")

        direction = payload.adjustment_direction.value

        if direction == "increase":
            inventory.stock += payload.quantity
        else:
            if inventory.stock < payload.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"No hay stock. Stock actual={inventory.stock}, Petición de={payload.quantity}"
                )
            inventory.stock -= payload.quantity
    else:
        raise HTTPException(status_code=400, detail="Movimiento inválido")

    inventoryMovement = InventoryMovement(
        inventory_id = payload.inventory_id,
        ticket_id = payload.ticket_id,
        movement_type = payload.movement_type.value,
        quantity = payload.quantity,
        reason = payload.reason.value if payload.reason else None,
        description = payload.description,
        unit_cost = payload.unit_cost,
        unit_price = payload.unit_price,
    )
    
    db.add(inventoryMovement)
    db.commit()
    db.refresh(inventoryMovement)
    return inventoryMovement