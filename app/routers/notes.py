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
    tags=["Keep Notes"]
)

# ---------------- CREATE NOTE ----------------
@note_router.post("/create_notes", response_model=dict)
def create_note(new_note: note.NoteBase, current_user: dict = Depends(AuthUsers.get_current_user), db: Session = Depends(database.get_db)):
    """Create a new note."""
    note_obj = Note(
        note_title=new_note.note_title,
        note_content=new_note.note_content,
        user_id=current_user["id"]
    )
    db.add(note_obj)
    db.commit()
    db.refresh(note_obj)
    return {"message": "Note created successfully", "note_id": note_obj.note_id}


# ---------------- FETCH ALL NOTES ----------------
@note_router.get("/fetch_all_notes", response_model=list[note.NoteResponse])
def get_notes(
    current_user: dict = Depends(AuthUsers.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Retrieve all notes belonging to the logged-in user."""
    user_id = current_user["id"]
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    return notes


# ---------------- UPDATE NOTE ----------------
@note_router.put("/update_note/{note_id}", response_model=dict)
def update_note(
    note_id: str,
    updated_note: note.NoteUpdate,
    current_user: dict = Depends(AuthUsers.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Update an existing note."""
    user_id = current_user["id"]
    note_obj = db.query(Note).filter(Note.note_id == note_id, Note.user_id == user_id).first()

    if not note_obj:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    note_obj.note_content = updated_note.note_content

    db.commit()
    db.refresh(note_obj)
    return {"message": "Note updated successfully", "note_id": note_obj.note_id}


# ---------------- DELETE NOTE ----------------
@note_router.delete("/delete_note/{note_id}", response_model=dict)
def delete_note(
    note_id: str,
    current_user: dict = Depends(AuthUsers.get_current_user),
    db: Session = Depends(database.get_db)
):
    """Delete a note by ID."""
    user_id = current_user["id"]
    note_obj = db.query(Note).filter(Note.note_id == note_id, Note.user_id == user_id).first()

    if not note_obj:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")

    db.delete(note_obj)
    db.commit()
    return {"message": "Note deleted successfully", "note_id": note_id}
