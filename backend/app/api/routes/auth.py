from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_database, get_current_user
from app.core.security import verify_password, hash_password, create_access_token
from app.models.user import User
from app.schemas.user import UserOut, UserCreate
from app.schemas.auth import Token, LoginRequest

router = APIRouter(prefix="/auths", tags=["auths"])

@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_database)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_database)):
    hashed_pw = hash_password(payload.password)
    user = User(email=payload.email, hashed_password=hashed_pw, role=payload.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user