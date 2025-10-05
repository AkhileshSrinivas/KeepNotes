"""
API endpoints for Notes CRUD operations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import database
from models.database import User, Note
from schemas import note
from services.verify import AuthUsers

note_router = APIRouter(
    tags=["Notebox window"]
)

@note_router.post("/create_notes", response_model=dict)
def create_note(new_note: note.NoteBase, current_user: dict = Depends(AuthUsers.get_current_user), db: Session = Depends(database.get_db)):
    """Create a new note."""
    note_obj = Note(note_title=new_note.note_title, note_content=new_note.note_content, user_id=current_user["id"])
    db.add(note_obj)
    db.commit()
    db.refresh(note_obj)
    return {"message": "Note created successfully", "note_id": note_obj.note_id}

@note_router.get("/fetch_all_notes", response_model=list[note.NoteResponse])
def get_notes(
    current_user: dict = Depends(AuthUsers.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Retrieve all notes belonging to the logged-in user."""
    user_id = current_user["id"]  

    notes = db.query(Note).filter(Note.user_id == user_id).all()
    return notes