from typing import Optional, List
from fastapi import FastAPI, status, Depends, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette.responses import Response
from .. import oauth, utils, models, schemas
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth.get_current_user),
              search: Optional[str] = "", limit: int = 10, skip: int = 0):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search)).limit(limit).offset(skip)\
        .all()
    return posts


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can not find post with id: {id}")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can not find post with id: {id}")
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can not find post with id: {id}")
    query.update(post.dict(), synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)



