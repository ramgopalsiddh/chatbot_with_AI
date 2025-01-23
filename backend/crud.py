from sqlalchemy.orm import Session
import models

def create_message(db: Session, user_message: str, bot_response: str):
    db_message = models.Message(user_message=user_message, bot_response=bot_response)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_all_messages(db: Session):
    return db.query(models.Message).all()

def get_query_response(db: Session, query: str):
    return db.query(models.Data).filter(models.Data.query == query).first()
