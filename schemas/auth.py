from pydantic import BaseModel, Field, EmailStr

class CreateUserSchema(BaseModel):
    username: str=Field(min_length=3)
    email: EmailStr
    first_name: str
    last_name: str
    password: str=Field(min_length=6)
    role:str
    
    class Config:
        json_schema_extra={
            'example':{
                'username': "User Name",
                'email': "youremail@example.com",
                'first_name': "You Name",
                'last_name': "You Last Name",
                'password': "Paswword",
                'role': 'admin'
            }
        }

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role:str
    
    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token:str
    token_type:str
    
    class Config:
        orm_mode = True
        json_schema_extra={
            'example':{
                'access_token': 'you_token',
                'token_type': 'type_token'
            }
        }

class LoginSchema(BaseModel):
    username:str
    password:str
    
    class Config:
        json_schema_extra={
            'example':{
                'password': "username",
                'password': "password"
            }
        }
