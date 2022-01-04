from fastapi import FastAPI, status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import Response
import sys
from .. import oauth, schemas, models, utils
from ..database import engine, get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Can not find user with id: {id}")

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
