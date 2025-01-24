from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from schemas import MessageCreate, MessageResponse
from crud import create_message, get_all_messages
from database import SessionLocal, engine

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
