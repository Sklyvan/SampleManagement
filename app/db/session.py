from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.api.configuration import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session for the lifetime of a request. We use a Python Generator to ensure that
    the finally block is executed to close the session after the request is processed. Using a return statement will be
    problematic as it will always exit the function immediately, and the finally block will not be executed.
    :return: SessionLocal
    """
    db = SessionLocal()
    try:
        # Ensure the database connection is established
        yield db
    finally:
        # Close the session to release resources
        db.close()
