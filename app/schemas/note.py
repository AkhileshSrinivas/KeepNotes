"""
Pydantic schemas for Notes (request/response models).
"""

from pydantic import BaseModel
from datetime import datetime

class NoteBase(BaseModel):
    note_title: str
    note_content: str | None = None

class NoteResponse(NoteBase):
    note_id: str
    user_id: str
    created_on: datetime
    last_update: datetime

    class Config:
        from_attributes = True
