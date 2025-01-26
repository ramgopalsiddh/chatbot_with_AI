from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import openai
import models
from schemas import MessageCreate, MessageResponse
from crud import create_message, get_all_messages
from database import SessionLocal, engine
from dotenv import load_dotenv
import os

# Set OpenAI API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# Function to get OpenAI response
def get_openai_response(user_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/messages/", response_model=MessageResponse)
def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    user_message = message.user_message

    # Get OpenAI response
    bot_response = get_openai_response(user_message)

    # Save the message and response to the database
    return create_message(db, user_message, bot_response)

@app.get("/messages/")
def get_messages(db: Session = Depends(get_db)):
    return get_all_messages(db)
