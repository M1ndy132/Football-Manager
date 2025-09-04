# app/routers/match_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.database.models import Match, Team
from app.schemas.match import MatchCreate, MatchResponse, MatchUpdate

router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    # Check if both teams exist
    team_a = db.query(Team).filter(Team.id == match.team_a_id).first()
    team_b = db.query(Team).filter(Team.id == match.team_b_id).first()

    if not team_a or not team_b:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="One or both teams not found"
        )

    # Check if a team is playing against itself
    if match.team_a_id == match.team_b_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A team cannot play against itself",
        )

    db_match = Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


@router.get("/", response_model=List[MatchResponse])
def get_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    matches = db.query(Match).offset(skip).limit(limit).all()
    return matches


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Match not found"
        )
    return match


@router.put("/{match_id}", response_model=MatchResponse)
def update_match(
    match_id: int, match_update: MatchUpdate, db: Session = Depends(get_db)
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Match not found"
        )

    for field, value in match_update.dict(exclude_unset=True).items():
        setattr(match, field, value)

    db.commit()
    db.refresh(match)
    return match


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Match not found"
        )

    db.delete(match)
    db.commit()
    return None


@router.get("/team/{team_id}", response_model=List[MatchResponse])
def get_team_matches(team_id: int, db: Session = Depends(get_db)):
    # Check if team exists
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )

    matches = (
        db.query(Match)
        .filter((Match.team_a_id == team_id) | (Match.team_b_id == team_id))
        .all()
    )
    return matches
