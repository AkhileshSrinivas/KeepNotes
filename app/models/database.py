"""
SQLAlchemy ORM models for User and Notes.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from db.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    user_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_on = Column(DateTime, default=datetime.utcnow)

    notes = relationship("Note", back_populates="owner")

class Note(Base):
    __tablename__ = "notes"

    note_id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    note_title = Column(String(200), nullable=False)
    note_content = Column(String(500), nullable=True)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_on = Column(DateTime, default=datetime.utcnow)

    user_id = Column(CHAR(36), ForeignKey("users.user_id"))
    owner = relationship("User", back_populates="notes")
