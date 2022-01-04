from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UserCreate(User):
    pass


class UserLogin(User):
    pass


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    type: str


class TokenData(BaseModel):
    id: int


class VoteBase(BaseModel):
    post_id: int
    user_id: int


class VoteIn(BaseModel):
    post_id: int
    vote_dir: int = 1

    class Config:
        orm_mode = True
