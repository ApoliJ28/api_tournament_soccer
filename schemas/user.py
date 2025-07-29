from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from models.user import RoleUserEnum

class CreateUserSchema(BaseModel):
    username: str=Field(min_length=3)
    dni:str
    email: EmailStr
    first_name: str
    last_name: str
    password: str=Field(min_length=6)
    role:RoleUserEnum
    
    class Config:
        json_schema_extra={
            'example':{
                'username': "User Name",
                'dni': '22555666',
                'email': "youremail@example.com",
                'first_name': "You Name",
                'last_name': "You Last Name",
                'password': "Paswword",
                'role': 'admin'
            }
        }

class UserSchema(BaseModel):
    username: str
    dni:str
    email: EmailStr
    first_name: str
    last_name: str
    role:RoleUserEnum
    
    class Config:
        orm_mode = True

class UpdateUserSchema(BaseModel):
    username: Optional[str]=Field(default=None, min_length=3) 
    dni:Optional[str]=None 
    email: Optional[EmailStr]=None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    role:Optional[RoleUserEnum]=None
    
    class Config:
        json_schema_extra={
            'example':{
                'username': "User Name",
                'dni': '22555666',
                'email': "youremail@example.com",
                'first_name': "You Name",
                'last_name': "You Last Name",
                'role': 'admin'
            }
        }

class ChangePasswordSchema(BaseModel):
    new_password:str
    
    class Config:
        json_schema_extra={
            'example':{
                'new_password': "Paswword"
            }
        }