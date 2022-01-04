from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, DATETIME, text, ForeignKey


class Post(Base):
    __tablename__ = "posts"
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(45), nullable=False)
    content = Column(String(10000), nullable=False)
    published = Column(Boolean, server_default='1')
    created_at = Column(DATETIME, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    # __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(45), nullable=False)
    password = Column(String(10000), nullable=False)
    created_at = Column(DATETIME, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
