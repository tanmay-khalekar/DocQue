from typing import Generator
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get DB session.

    Ensures:
    - session is created per request
    - session is closed after request
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()