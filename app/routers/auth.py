from typing import Optional, List
from fastapi import FastAPI, status, Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import Response
from .. import oauth, utils, models, schemas
from ..database import engine, get_db

router = APIRouter(
    tags=["Authentication"]
)

router = APIRouter()


@router.post("/login")
def login(user_input: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_input.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials email")

    if not utils.verify(user_input.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid Credentials")

    # create token
    access_token = oauth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
