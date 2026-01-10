from fastapi import APIRouter

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/")
def list_tickets():
    return[]