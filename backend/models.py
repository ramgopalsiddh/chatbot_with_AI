from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.now)

class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, unique=True, nullable=False)
    response = Column(Text, nullable=False)
