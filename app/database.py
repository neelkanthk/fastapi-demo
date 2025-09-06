from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from app.config import driver, host, username, password, port, database_name

# Database URL from environment variable or default to local PostgreSQL
SQLALCHEMY_DATABASE_URL = f"{driver}://{username}:{password}@{host}:{port}/{database_name}"

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
