from .database import Base
from sqlalchemy import Column, INTEGER, VARCHAR, TEXT, BOOLEAN, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(INTEGER, primary_key=True, nullable=False)
    title = Column(VARCHAR, nullable=False)
    content = Column(TEXT, nullable=False)
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    published = Column(BOOLEAN, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    updated_at = Column(TIMESTAMP, nullable=True)

    author = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True, nullable=False)
    email = Column(VARCHAR, nullable=False, unique=True)
    password = Column(VARCHAR, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(INTEGER, ForeignKey("posts.id"), primary_key=True)
    user_id = Column(INTEGER, ForeignKey("users.id"), primary_key=True)
