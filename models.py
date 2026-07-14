from pydantic import BaseModel


class UserReg(BaseModel):
    name: str
    username: str
    email: str
    h_pwd: str
class UserLogin(BaseModel):
    username: str
    h_pwd: str

class pr(BaseModel):
    id : int
    name : str
    username : str
class protected_response(BaseModel):
    user : pr
class RefreshRequest(BaseModel):
    refresh_token: str

class Insert_note(BaseModel):
    title: str
    content: str
class Update_note(BaseModel):
    id:int
    title: str
    content: str
    
class Get_note(BaseModel):
    title: str
    content: str