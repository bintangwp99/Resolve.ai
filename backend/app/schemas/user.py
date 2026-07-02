from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserInDBBase(UserBase):
    id: int
    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass
    
class Token(BaseModel):
    access_token: str
    token_type: str
