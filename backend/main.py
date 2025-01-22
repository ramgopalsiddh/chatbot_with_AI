from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from crud import create_message, get_all_messages
from database import SessionLocal, engine
from pydantic import BaseModel
from datetime import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MessageCreate(BaseModel):
    user_message: str

class MessageResponse(BaseModel):
    id: int
    user_message: str
    bot_response: str
    timestamp: datetime

    class Config:
        orm_mode = True


@app.post("/messages/", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    user_message = message.user_message
    # Basic bot response logic
    if "hello" in user_message.lower():
        bot_response = "Hi! How can I help you?"
    else:
        bot_response = "Sorry, I didn't understand that."

    return create_message(db, user_message, bot_response)

@app.get("/messages/")
def get_messages(db: Session = Depends(get_db)):
    return get_all_messages(db)
