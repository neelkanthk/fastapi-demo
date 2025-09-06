from fastapi import FastAPI, status

from fastapi.responses import JSONResponse
import logging
import app.models as models
import app.database as database
from app.routers.post import router as post_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.vote import router as vote_router
from datetime import datetime

app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)
logger = logging.getLogger("uvicorn.error")

# Create DB tables if not exist
models.Base.metadata.create_all(bind=database.engine)


@app.get('/', status_code=status.HTTP_200_OK)
def read_root():
    return JSONResponse(content={
        "message": "Welcome to FastAPI Posts API Service !",
        "time": datetime.now().isoformat(),
        "database": "Connected" if database.get_db else "Not Connected"
    }, status_code=status.HTTP_200_OK)
