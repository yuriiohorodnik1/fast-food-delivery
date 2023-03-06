from config.database import SessionLocal


def get_db():
    """Get session instance to perform SLQ operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
