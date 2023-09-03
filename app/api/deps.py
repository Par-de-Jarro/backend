from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.user.services.user_service import UserService


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:  # noqa: E722
        db.rollback()
        raise
    else:
        if db.is_active:
            db.commit()
    finally:
        db.close()


def get_service(db: Session = Depends(get_db)):
    return UserService(db)


def hass_access(db: Session = Depends(get_db)):
    return UserService(db)


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)
