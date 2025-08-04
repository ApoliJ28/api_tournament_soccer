from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from typing import Annotated, Optional, List
from sqlalchemy.orm import Session

from database.db import SessionLocal
from .auth import get_current_user
from models.coach import Coach
from models.team import Team
from schemas.coach import CoachSchema, UpdateCoachSchema
from schemas.common import PaginatedResponse
from routes.auth import bycrypt_context

router = APIRouter(
    prefix='api/coach',
    tags=['coach'],
    include_in_schema=True
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependecy = Annotated[Session, Depends(get_db)]
user_dependecy = Annotated[dict, Depends(get_current_user)]

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CoachSchema)
async def get_coach(user: user_dependecy, db:db_dependecy, id:int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message': "User not authorized",
            'success': False,
            'payload': []
        })
    
    coach_db = db.query(Coach).filter(Coach.id == id).first()
    
    if coach_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'message': "Coach not found",
            'success': False,
            'payload': []
        })
    
    return coach_db

@router.get('/', status_code=status.HTTP_200_OK, response_model=PaginatedResponse[CoachSchema])
async def get_coachs(user: user_dependecy, db:db_dependecy, 
                    skip:int = Query(default=0, ge=0), limit:int = Query(default=10, ge=1),
                    team_id: Optional[int] = Query(default=None)
                    ):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message': "User not authorized",
            'success': False,
            'payload': []
        })
    
    query = db.query(Coach)
    
    if team_id:
        query = query.join(Coach.team).filter(Team.id == team_id).first()
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    page = (skip / limit) + 1
    pages = (total + limit - 1) // limit
    
    if items is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'message': "Coachs not founds",
            'success': False,
            'payload': []
        })
    
    return PaginatedResponse[CoachSchema](
        skip=skip,
        limit=limit,
        total=total,
        page=page,
        limit=limit,
        pages=pages,
        payload=items
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CoachSchema)
async def created_coach(
            user: user_dependecy, db:db_dependecy,
            coach_schema: CoachSchema = Body(..., examples=CoachSchema.Config.json_schema_extra['example'])
            ):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message': "User not authorized",
            'success': False,
            'payload': []
        })
    
    query = db.query(Coach).filter(Coach.dni == coach_schema.dni).first()
    
    if query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            'message': "DNI already exist, not create coach... Try again",
            'success': False,
            'payload': []
        })
    
    coach = Coach(**coach_schema.model_dump(exclude_unset=True))
    
    try:
        db.add(coach)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            'message': f"Coach not created, error: {e}",
            'success': False,
            'payload': []
        })
    else:
        db.commit()
        
        return coach

@router.path("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=CoachSchema)
async def updated_coach(
            user: user_dependecy, db:db_dependecy,
            id:int,
            coach_updated_schema: UpdateCoachSchema = 
            Body(..., examples=UpdateCoachSchema.Config.json_schema_extra['example'])
            ):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message': "User not authorized",
            'success': False,
            'payload': []
        })
    
    coach_db = db.query(Coach).filter(Coach.id == id).first()
    
    if coach_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            'message': "Coach not found.",
            'success': False,
            'payload': []
        })
    
    data = coach_updated_schema.model_dump(exclude_unset=True)
    
    for key, value in data.items():
        setattr(coach_db, key, value)
    
    db.commit()
    return

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=CoachSchema)
async def updated_coach(
            user: user_dependecy, db:db_dependecy,
            id:int
            ):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            'message': "User not authorized",
            'success': False,
            'payload': []
        })
    
    coach_db = db.query(Coach).filter(Coach.id == id).first()
    
    if coach_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            'message': "Coach not found.",
            'success': False,
            'payload': []
        })
    
    db.delete(coach_db)
    
    db.commit()
    
    return coach_db
