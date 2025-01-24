from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    user_message: str

class MessageResponse(BaseModel):
    id: int
    user_message: str
    bot_response: str
    timestamp: datetime

    class Config:
        orm_mode = True
