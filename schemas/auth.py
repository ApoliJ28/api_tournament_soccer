from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token:str
    token_type:str
    
    class Config:
        from_attributes = True
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
