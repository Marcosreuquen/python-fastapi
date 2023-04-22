from ..utils import jwt
from ..models import models
from ..utils import schemas
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from ..models.database import get_db
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash pass
    user.password = jwt.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
async def get_post(id: UUID, response: Response, db: Session = Depends(get_db)):
    User = db.query(models.User).filter(models.User.id == id).first()
    if not User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} was not found"
        )
    return User
