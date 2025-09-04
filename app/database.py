from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/db_fastapi"

# Create SQLAlchemy engine to connect to pgsql
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our application's models
Base = declarative_base()

# Function to get session to the database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
