"""
Coach service for Football League Manager.

Contains business logic for coach management, including
CRUD operations and coach-team relationships.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import (
    CoachNotFoundException,
    DuplicateResourceException,
    TeamNotFoundException,
)
from app.database.models import Coach, Team
from app.schemas.coach import CoachCreate, CoachUpdate


def get_coach(db: Session, coach_id: int) -> Coach:
    """Get a coach by ID."""
    coach = db.query(Coach).filter(Coach.id == coach_id).first()
    if not coach:
        raise CoachNotFoundException(f"Coach with id {coach_id} not found")
    return coach


def get_coach_by_name(db: Session, name: str) -> Optional[Coach]:
    """Get a coach by name."""
    return db.query(Coach).filter(Coach.name == name).first()


def get_coaches(db: Session, skip: int = 0, limit: int = 100) -> List[Coach]:
    """Get all coaches with pagination."""
    return db.query(Coach).offset(skip).limit(limit).all()


def get_coaches_by_team(db: Session, team_id: int) -> List[Coach]:
    """Get all coaches for a specific team."""
    # Verify team exists
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise TeamNotFoundException(f"Team with id {team_id} not found")

    return db.query(Coach).filter(Coach.team_id == team_id).all()


def create_coach(db: Session, coach: CoachCreate) -> Coach:
    """Create a new coach."""
    # Verify team exists if team_id is provided
    if coach.team_id:
        team = db.query(Team).filter(Team.id == coach.team_id).first()
        if not team:
            raise TeamNotFoundException(f"Team with id {coach.team_id} not found")

    # Check if coach with same name already exists in the same team
    if coach.team_id:
        existing_coach = (
            db.query(Coach)
            .filter(Coach.name == coach.name, Coach.team_id == coach.team_id)
            .first()
        )
        if existing_coach:
            raise DuplicateResourceException(
                f"Coach '{coach.name}' already exists in this team"
            )

    db_coach = Coach(**coach.model_dump())
    db.add(db_coach)
    db.commit()
    db.refresh(db_coach)
    return db_coach


def update_coach(db: Session, coach_id: int, coach_update: CoachUpdate) -> Coach:
    """Update an existing coach."""
    db_coach = get_coach(db, coach_id)

    update_data = coach_update.model_dump(exclude_unset=True)

    # Verify team exists if team_id is being updated
    if "team_id" in update_data and update_data["team_id"]:
        team = db.query(Team).filter(Team.id == update_data["team_id"]).first()
        if not team:
            raise TeamNotFoundException(
                f"Team with id {update_data['team_id']} not found"
            )

    for field, value in update_data.items():
        setattr(db_coach, field, value)

    db.commit()
    db.refresh(db_coach)
    return db_coach


def delete_coach(db: Session, coach_id: int) -> bool:
    """Delete a coach."""
    db_coach = get_coach(db, coach_id)
    db.delete(db_coach)
    db.commit()
    return True


def get_coaches_by_specialization(db: Session, specialization: str) -> List[Coach]:
    """Get coaches by their specialization."""
    return db.query(Coach).filter(Coach.specialization == specialization).all()


def get_coaches_by_nationality(db: Session, nationality: str) -> List[Coach]:
    """Get coaches by nationality."""
    return db.query(Coach).filter(Coach.nationality == nationality).all()


def get_coach_statistics(db: Session, coach_id: int) -> dict:
    """Get coach statistics and profile information."""
    coach = get_coach(db, coach_id)

    return {
        "coach_id": coach.id,
        "name": coach.name,
        "team_id": coach.team_id,
        "experience_years": coach.experience_years,
        "specialization": coach.specialization,
        "nationality": coach.nationality,
        # Additional statistics would go here based on your tracking needs
        "matches_coached": 0,  # Placeholder - would query actual match data
        "wins": 0,  # Placeholder
        "losses": 0,  # Placeholder
        "draws": 0,  # Placeholder
        "win_percentage": 0.0,  # Placeholder
    }


def transfer_coach(db: Session, coach_id: int, new_team_id: int) -> Coach:
    """Transfer a coach to a new team."""
    coach = get_coach(db, coach_id)

    # Verify new team exists
    new_team = db.query(Team).filter(Team.id == new_team_id).first()
    if not new_team:
        raise TeamNotFoundException(f"Team with id {new_team_id} not found")

    setattr(coach, "team_id", new_team_id)
    db.commit()
    db.refresh(coach)
    return coach
