from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logger import get_logger
from app.database.init_db import init_database
from app.api.router import api_router

logger = get_logger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    init_database()
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
app.include_router(api_router)

@app.get("/")
def root():
    logger.info("Root endpoint called")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
    }