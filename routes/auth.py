from fastapi import APIRouter, Depends, HTTPException, status, Body
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone

from settings import Settings
from schemas.auth import  TokenSchema, LoginSchema
from schemas.user import CreateUserSchema, UserSchema
from models.user import User
from database.db import SessionLocal

setting = Settings()

router = APIRouter(
    prefix='/api/auth',
    tags=['auth'],
    include_in_schema=True
)

bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl=router.prefix+"/token/form")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]

def authenticate_user(username:str, password:str, db: db_dependecy):
    user= db.query(User).filter(User.username==username).first()
    
    if not user:
        return False
    
    if not bycrypt_context.verify(password, user.password):
        return False
    
    return user

def create_access_token(username:str, user_id:int, role:str, dni:str, expires_delta:timedelta):
    token_encode = {
        'username': username,
        'user_id': user_id,
        'dni': dni,
        'role': role
    }
    
    expires = datetime.now(timezone.utc) + expires_delta
    token_encode.update({'exp': expires})
    
    return jwt.encode(token_encode, setting.secret_key, algorithm=setting.algorithm)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    try:
        
        payload = jwt.decode(token, setting.secret_key, algorithms=setting.algorithm)
        username = payload.get('username')
        id = payload.get('user_id')
        dni = payload.get('dni')
        role = payload.get('role')
        
        if username is None or id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                'message': "User not authorized",
                'success': False,
                'payload': []
            })
        
        return {'username': username, 'user_id': id, 'role': role, 'dni' : dni}
    
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                'message': f"User not authorized, error: {e}",
                'success': False,
                'payload': []
            })

user_dependecy = Annotated[dict, Depends(get_current_user)]

@router.post('/', status_code=status.HTTP_201_CREATED, include_in_schema=True, response_model=UserSchema)
async def create_user(user: user_dependecy, db: db_dependecy,  user_body: CreateUserSchema):
    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message': "User not authorized",
            'success': False,
            'payload': []
        })
    
    user_db = db.query(User).filter( (User.username == user_body.username) | (User.email == user_body.email) | (User.dni == user_body.dni) ).first()
    
    if user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            'message': "Username or Email or DNI already exist.",
            'success': False,
            'payload': []
        })
    
    user_body.password = bycrypt_context.hash(user_body.password)
    
    user = User(**user_body.model_dump(exclude_unset=True))
    
    try:
        db.add(user)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            'message': f"User not created, error: {e}",
            'success': False,
            'payload': []
        })
    else:
        db.commit()
        
        return user

@router.post('/token/form', response_model=TokenSchema, include_in_schema=False)
async def login_for_access_token_form(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependecy):
    user=authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message':"User not authorized.",
            'succcess':False,
            'payload':[]
            })
    
    token=create_access_token(user.username, user.id, user.role, user.dni, timedelta(minutes=60))
    return {'access_token':token, 'token_type':'bearer'}

@router.post('/token', response_model=TokenSchema)
async def login_for_access_token( db: db_dependecy, login_data: LoginSchema = Body(..., examples=LoginSchema.Config.json_schema_extra['example'])):
    user = authenticate_user(login_data.username, login_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'message': "User not authorized.",
                'succcess': False,
                'payload': []
            }
        )

    token = create_access_token(user.username, user.id, user.role, user.dni, timedelta(minutes=60))
    return {'access_token': token, 'token_type': 'bearer'}
