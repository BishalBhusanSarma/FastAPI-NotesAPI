from fastapi import APIRouter, Depends, HTTPException
from models import UserReg, RefreshRequest, protected_response, Insert_note, Update_note
from fastapi.security import OAuth2PasswordRequestForm
from all_functions import verify_password, create_access_token, create_refresh_token, verify_access_token, verify_refresh_token
from db import create_user, get_by_email, get_by_username, insert_note, show_notes, update_notes, delete_notes

router = APIRouter(prefix="/notesapi", tags=["Auth"])


@router.post("/register_user")
def register_user(user:UserReg):
    return create_user(user)

@router.post("/login")
def login_user(user:OAuth2PasswordRequestForm = Depends()):
    user_details = get_by_username(user.username) or get_by_email(user.username)
    if user_details is None:
        raise HTTPException(status_code=401, detail="Invalid username")
    pwd = verify_password(user.password, user_details["hashed_password"])
    if not pwd:
        raise HTTPException(status_code=401, detail="Invalid password")
    username = user_details["username"]
    return {"access_token": create_access_token(username),
            "refresh_token": create_refresh_token(username),
            "token_type": "bearer"}

@router.post("/refresh")
def refresh(data:RefreshRequest):
    payload = verify_refresh_token(data.refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="not a refresh token")
    if payload["type"] != "refresh":
        raise HTTPException(status_code=401, detail="not a refresh token")
    username = payload["sub"]

    new_access_token = create_access_token(username)
    return {"new_access_token": new_access_token, "type": "bearer"}

