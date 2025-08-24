from database import Base
from sqlalchemy import Column, INTEGER, VARCHAR, TEXT, BOOLEAN, TIMESTAMP


class Post(Base):
    __tablename__ = 'posts'

    id = Column(INTEGER, primary_key=True, nullable=False)
    title = Column(VARCHAR, nullable=False)
    content = Column(TEXT, nullable=False)
    author = Column(VARCHAR, nullable=False)
    published = Column(BOOLEAN, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)
