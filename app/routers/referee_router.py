# app/routers/referee_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.database.models import Referee
from app.schemas.referee import RefereeCreate, RefereeResponse, RefereeUpdate

router = APIRouter(prefix="/referees", tags=["referees"])

@router.post("/", response_model=RefereeResponse, status_code=status.HTTP_201_CREATED)
def create_referee(referee: RefereeCreate, db: Session = Depends(get_db)):
    db_referee = Referee(**referee.dict())
    db.add(db_referee)
    db.commit()
    db.refresh(db_referee)
    return db_referee

@router.get("/", response_model=List[RefereeResponse])
def get_referees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    referees = db.query(Referee).offset(skip).limit(limit).all()
    return referees

@router.get("/{referee_id}", response_model=RefereeResponse)
def get_referee(referee_id: int, db: Session = Depends(get_db)):
    referee = db.query(Referee).filter(Referee.id == referee_id).first()
    if not referee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referee not found"
        )
    return referee

@router.get("/experience/{min_experience}", response_model=List[RefereeResponse])
def get_referees_by_experience(min_experience: int, db: Session = Depends(get_db)):
    referees = db.query(Referee).filter(Referee.experience_years >= min_experience).all()
    return referees

@router.put("/{referee_id}", response_model=RefereeResponse)
def update_referee(referee_id: int, referee_update: RefereeUpdate, db: Session = Depends(get_db)):
    referee = db.query(Referee).filter(Referee.id == referee_id).first()
    if not referee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referee not found"
        )
    
    for field, value in referee_update.dict(exclude_unset=True).items():
        setattr(referee, field, value)
    
    db.commit()
    db.refresh(referee)
    return referee

@router.delete("/{referee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_referee(referee_id: int, db: Session = Depends(get_db)):
    referee = db.query(Referee).filter(Referee.id == referee_id).first()
    if not referee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Referee not found"
        )
    
    db.delete(referee)
    db.commit()
    return None
