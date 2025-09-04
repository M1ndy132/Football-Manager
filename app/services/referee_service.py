"""
Referee service for Football League Manager.

Contains business logic for referee management, including
CRUD operations and referee scheduling.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.models import Referee, Match
from app.schemas.referee import RefereeCreate, RefereeUpdate
from app.core.exceptions import RefereeNotFoundException, DuplicateResourceException


def get_referee(db: Session, referee_id: int) -> Referee:
    """Get a referee by ID."""
    referee = db.query(Referee).filter(Referee.id == referee_id).first()
    if not referee:
        raise RefereeNotFoundException(f"Referee with id {referee_id} not found")
    return referee


def get_referee_by_name(db: Session, name: str) -> Optional[Referee]:
    """Get a referee by name."""
    return db.query(Referee).filter(Referee.name == name).first()


def get_referees(db: Session, skip: int = 0, limit: int = 100) -> List[Referee]:
    """Get all referees with pagination."""
    return db.query(Referee).offset(skip).limit(limit).all()


def create_referee(db: Session, referee: RefereeCreate) -> Referee:
    """Create a new referee."""
    # Check if referee with same name already exists
    existing_referee = get_referee_by_name(db, referee.name)
    if existing_referee:
        raise DuplicateResourceException(f"Referee with name '{referee.name}' already exists")
    
    db_referee = Referee(**referee.model_dump())
    db.add(db_referee)
    db.commit()
    db.refresh(db_referee)
    return db_referee


def update_referee(db: Session, referee_id: int, referee_update: RefereeUpdate) -> Referee:
    """Update an existing referee."""
    db_referee = get_referee(db, referee_id)
    
    update_data = referee_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_referee, field, value)
    
    db.commit()
    db.refresh(db_referee)
    return db_referee


def delete_referee(db: Session, referee_id: int) -> bool:
    """Delete a referee."""
    db_referee = get_referee(db, referee_id)
    db.delete(db_referee)
    db.commit()
    return True


def get_referees_by_nationality(db: Session, nationality: str) -> List[Referee]:
    """Get referees by nationality."""
    return db.query(Referee).filter(Referee.nationality == nationality).all()


def get_referee_statistics(db: Session, referee_id: int) -> dict:
    """Get referee statistics and profile information."""
    referee = get_referee(db, referee_id)
    
    return {
        "referee_id": referee.id,
        "name": referee.name,
        "experience_years": referee.experience_years,
        "nationality": referee.nationality,
        # Additional statistics would go here based on your tracking needs
        "matches_officiated": 0,  # Placeholder - would query actual match data
        "yellow_cards_issued": 0,  # Placeholder
        "red_cards_issued": 0,  # Placeholder
        "penalties_awarded": 0,  # Placeholder
    }

