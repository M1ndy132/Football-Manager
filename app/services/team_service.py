"""
Team service for Football League Manager.

Contains business logic for team management, including
CRUD operations and team-related business rules.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.models import Team
from app.schemas.team import TeamCreate, TeamUpdate
from app.core.exceptions import TeamNotFoundException, DuplicateResourceException


def get_team(db: Session, team_id: int) -> Team:
    """Get a team by ID."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise TeamNotFoundException(f"Team with id {team_id} not found")
    return team


def get_team_by_name(db: Session, name: str) -> Optional[Team]:
    """Get a team by name."""
    return db.query(Team).filter(Team.name == name).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100) -> List[Team]:
    """Get all teams with pagination."""
    return db.query(Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: TeamCreate) -> Team:
    """Create a new team."""
    # Check if team with same name already exists
    existing_team = get_team_by_name(db, team.name)
    if existing_team:
        raise DuplicateResourceException(f"Team with name '{team.name}' already exists")
    
    db_team = Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def update_team(db: Session, team_id: int, team_update: TeamUpdate) -> Team:
    """Update an existing team."""
    db_team = get_team(db, team_id)
    
    update_data = team_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_team, field, value)
    
    db.commit()
    db.refresh(db_team)
    return db_team


def delete_team(db: Session, team_id: int) -> bool:
    """Delete a team."""
    db_team = get_team(db, team_id)
    db.delete(db_team)
    db.commit()
    return True


def get_team_players(db: Session, team_id: int):
    """Get all players for a specific team."""
    from app.database.models import Player
    team = get_team(db, team_id)
    return db.query(Player).filter(Player.team_id == team.id).all()


def get_team_matches(db: Session, team_id: int):
    """Get all matches for a specific team."""
    from app.database.models import Match
    team = get_team(db, team_id)
    return db.query(Match).filter(
        (Match.team_a_id == team.id) | (Match.team_b_id == team.id)
    ).all()
