from passlib.context import CryptContext
from jose import jwt, JWTError
from models import UserLogin
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXP = int(os.getenv("ACCESS_TOKEN_EXP"))
REFRESH_TOKEN_EXP = int(os.getenv("REFRESH_TOKEN_EXP"))

password_context = CryptContext(schemes=["argon2"], deprecated = "auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="notesapi/login")

def create_hash_pwd(password:str):
    return password_context.hash(password)

def verify_password(plain_pwd, hsd_pwd):
    return password_context.verify(plain_pwd, hsd_pwd)


def create_access_token(username: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXP)
    payload = {"sub": username,"type": "access", "exp": exp}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(username: str):
    
    exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXP)
    payload = {"sub": username,"type": "refresh", "exp": exp}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    

def verify_access_token(token:str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload["sub"]
        if username is None:
            raise HTTPException(status_code=401, detail="token expired")
        if payload["type"] != "access":
            raise HTTPException(status_code=401, detail="Not a valid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Not a valid token")

def verify_refresh_token(token:str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="Not a valid token")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Not a valid token")
    