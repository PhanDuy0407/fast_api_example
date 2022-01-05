from typing import Optional, List
from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from app import models
from app.database import engine, get_db
from app.routers import user, post, auth, vote
from sqlalchemy import MetaData


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    print(models.Base.metadata.tables)
    return {"message": "Hello, world"}
#
#
# @app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts
#
#
# @app.get("/posts/{id}")
# def get_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can not find post with id: {id}")
#     return post
#
#
# # @app.get("/sqlalchemy")
# # def test_post(db: Session = Depends(get_db)):
# #     return {"message": "success"}
#
#
# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post
#
#
# @app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     query = db.query(models.Post).filter(models.Post.id == id)
#     post = query.first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can not find post with id: {id}")
#     query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#
#
# @app.put("/update/{id}")
# def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
#     query = db.query(models.Post).filter(models.Post.id == id)
#     if not query.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can not find post with id: {id}")
#     query.update(post.dict(), synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_200_OK)
#
#
# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
# def create_user(user: schemas.User, db: Session = Depends(get_db)):
#     user.password = utils.hash(user.password)
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
