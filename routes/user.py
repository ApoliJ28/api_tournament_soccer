from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from typing import Annotated, Optional, List
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone

from database.db import SessionLocal
from .auth import get_current_user
from models.user import User
from schemas.user import UserSchema, UpdateUserSchema, ChangePasswordSchema
from routes.auth import bycrypt_context

router = APIRouter(
    prefix='/api/user',
    tags=['user'],
    include_in_schema=True
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]

@router.get('/profile', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(user: user_dependecy, db:db_dependecy):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message': "User not authorized",
            'success': False,
            'payload': []
        })
    
    user_db = db.query(User).filter(User.id == user.get('user_id')).first()
    
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'message': "User not found",
            'success': False,
            'payload': []
        })
    
    return user_db

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def get_users(user: user_dependecy, db: db_dependecy, active: Optional[bool] = Query(True, description="Filter By active/inactive users")):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message': "User not authorized",
            'success': False,
            'payload': []
        })
    
    users_db = db.query(User).filter(User.is_active == active)
    
    if users_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'message': "User not found",
            'success': False,
            'payload': []
        })
    
    return users_db

@router.patch('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: user_dependecy, db: db_dependecy, id: int, user_updt : UpdateUserSchema = Body(..., examples=UpdateUserSchema.Config.json_schema_extra['example'])):
    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message': "User not authorized",
            'success': False,
            'payload': []
        })
    
    user_db = db.query(User).filter(User.id == id).first()
    
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'message': "User not found",
            'success': False,
            'payload': []
        })
    
    data = user_updt.model_dump(exclude_unset=True)
    
    for key, value in data.items():
        setattr(user_db, key, value)
    
    db.commit()
    return

@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependecy, db: db_dependecy, chamge_pass: ChangePasswordSchema = Body(..., examples=ChangePasswordSchema.Config.json_schema_extra['example']), id: Optional[int] = Query(None, description="Id to change the user's password")):
    if user is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail={
                            'message':"Not authorized.",
                            'data':[],
                            'succcess':False,
                            'error':'Authentication Failed'
                            })
    
    user_id = user.get('user_id') if id is None else id
    
    user_model = db.query(User).filter(User.id == user_id).first()
    
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_model.password = bycrypt_context.hash(chamge_pass.new_password)
    db.add(user_model)
    db.commit()
