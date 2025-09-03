# app/routers/coach_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.database.models import Coach, Team
from app.schemas.coach import CoachCreate, CoachResponse, CoachUpdate

router = APIRouter(prefix="/coaches", tags=["coaches"])

@router.post("/", response_model=CoachResponse, status_code=status.HTTP_201_CREATED)
def create_coach(coach: CoachCreate, db: Session = Depends(get_db)):
    # Check if team exists
    team = db.query(Team).filter(Team.id == coach.team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    db_coach = Coach(**coach.dict())
    db.add(db_coach)
    db.commit()
    db.refresh(db_coach)
    return db_coach

@router.get("/", response_model=List[CoachResponse])
def get_coaches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    coaches = db.query(Coach).offset(skip).limit(limit).all()
    return coaches

@router.get("/{coach_id}", response_model=CoachResponse)
def get_coach(coach_id: int, db: Session = Depends(get_db)):
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coach not found"
        )
    return coach

@router.get("/team/{team_id}", response_model=List[CoachResponse])
def get_team_coaches(team_id: int, db: Session = Depends(get_db)):
    # Check if team exists
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    
    coaches = db.query(Coach).filter(Coach.team_id == team_id).all()
    return coaches

@router.put("/{coach_id}", response_model=CoachResponse)
def update_coach(coach_id: int, coach_update: CoachUpdate, db: Session = Depends(get_db)):
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coach not found"
        )
    
    for field, value in coach_update.dict(exclude_unset=True).items():
        setattr(coach, field, value)
    
    db.commit()
    db.refresh(coach)
    return coach

@router.delete("/{coach_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coach(coach_id: int, db: Session = Depends(get_db)):
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coach not found"
        )
    
    db.delete(coach)
    db.commit()
    return None