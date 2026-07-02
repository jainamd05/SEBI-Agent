from app.core.logger import get_logger
from app.database.db import Base, engine

# Import models so SQLAlchemy registers them
from app.database import models

logger = get_logger(__name__)


def init_database() -> None:
    """
    Create all database tables if they do not already exist.
    """
    logger.info("Initializing database...")

    Base.metadata.create_all(bind=engine)

    logger.info("Database initialized successfully.")