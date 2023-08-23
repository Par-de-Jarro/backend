from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.todo.services.todo import TodoService


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


def get_todo_sevice(db: Session = Depends(get_db)):
    return TodoService(db)
