from fastapi import FastAPI
from app.api.routes.tickets import router as tickets_router
from app.api.routes.clients import router as clients_router
from app.api.routes.devices import router as devices_router
from app.api.routes.inventories import router as inventory_router
from app.api.routes.inventoryMovements import router as inventory_movements_route
from app.core.database import Base, engine #Esto es momentaneo, en un futuro se usara Asemblic
import app.models

app = FastAPI(title="PC Hub")

@app.get("/ok")
def health():
    return {"message": "All is ok"}

app.include_router(clients_router)
app.include_router(tickets_router)
app.include_router(devices_router)
app.include_router(inventory_router)
app.include_router(inventory_movements_route)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)