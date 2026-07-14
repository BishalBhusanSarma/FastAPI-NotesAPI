from fastapi import APIRouter, Depends
from models import Insert_note, Update_note

from all_functions import verify_access_token, verify_refresh_token
from db import  insert_note, show_notes, update_notes, delete_notes

router = APIRouter(prefix="/notesapi", tags=["Notes"])
@router.post("/create_note")
def create_note(note: Insert_note, name: str = Depends(verify_access_token)):
    return insert_note(name, note)

@router.get("/show_notes")
def get_notes(name: str = Depends(verify_access_token)):
    return show_notes(name)

@router.put("/update_notes")
def update_note(note: Update_note, username:str = Depends(verify_access_token)):
    return update_notes(username, note)

@router.delete("/delete_note")
def delete_note(note_id:int, username:str = Depends(verify_access_token)):
    return delete_notes(username, note_id)