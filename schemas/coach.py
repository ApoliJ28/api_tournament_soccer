from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class CoachSchema(BaseModel):
    first_name:str
    last_name:str
    dni:str = Field(max_length=8)
    photo_url:Optional[str]=None
    birth_date:date

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example":{
                "first_name": "Jackson",
                "last_name": "Lopez",
                "dni": "20564896",
                "photo_url": r"C:\Users\FINANZAS01\Documents\workspace\apoli\api_torneo_forum_backend\schemas\static\img\photo.png",
                "birth_date": "1989-06-25"
            }
        }

class UpdateCoachSchema(BaseModel):
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    dni: Optional[str] = Field(default=None ,max_length=8)
    photo_url:Optional[str]=None
    birth_date:Optional[date]=None
    
    class Config:
        json_schema_extra = {
            "example":{
                "first_name": "Jose",
                "last_name": "Lopez",
                "dni": "20564896",
                "photo_url": r"C:\Users\FINANZAS01\Documents\workspace\apoli\api_torneo_forum_backend\schemas\static\img\photo.png",
                "birth_date": "1989-06-25"
            }
        }
