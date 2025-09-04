from fastapi import FastAPI, status, Depends, HTTPException

from fastapi.responses import JSONResponse
import logging
import app.models as models
import app.database as database
from app.routers.post import router as post_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from datetime import datetime, timezone

app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
logger = logging.getLogger("uvicorn.error")

# Create DB tables if not exist
models.Base.metadata.create_all(bind=database.engine)


@app.get('/', status_code=status.HTTP_200_OK)
def read_root():
    return JSONResponse(content={
        "message": "Welcome to FastAPI",
        "time": datetime.now().isoformat()
    }, status_code=status.HTTP_200_OK)
