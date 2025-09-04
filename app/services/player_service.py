"""
Player service for Football League Manager.

Contains business logic for player management, including
CRUD operations and player statistics.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicateResourceException,
    PlayerNotFoundException,
    TeamNotFoundException,
)
from app.database.models import Player, Team
from app.schemas.player import PlayerCreate, PlayerUpdate


def get_player(db: Session, player_id: int) -> Player:
    """Get a player by ID."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise PlayerNotFoundException(f"Player with id {player_id} not found")
    return player


def get_player_by_name(db: Session, name: str) -> Optional[Player]:
    """Get a player by name."""
    return db.query(Player).filter(Player.name == name).first()


def get_players(db: Session, skip: int = 0, limit: int = 100) -> List[Player]:
    """Get all players with pagination."""
    return db.query(Player).offset(skip).limit(limit).all()


def get_players_by_team(db: Session, team_id: int) -> List[Player]:
    """Get all players for a specific team."""
    # Verify team exists
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise TeamNotFoundException(f"Team with id {team_id} not found")

    return db.query(Player).filter(Player.team_id == team_id).all()


def create_player(db: Session, player: PlayerCreate) -> Player:
    """Create a new player."""
    # Check if player with same name already exists in the same team
    existing_player = (
        db.query(Player)
        .filter(Player.name == player.name, Player.team_id == player.team_id)
        .first()
    )
    if existing_player:
        raise DuplicateResourceException(
            f"Player '{player.name}' already exists in this team"
        )

    # Verify team exists if team_id is provided
    if player.team_id:
        team = db.query(Team).filter(Team.id == player.team_id).first()
        if not team:
            raise TeamNotFoundException(f"Team with id {player.team_id} not found")

    db_player = Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def update_player(db: Session, player_id: int, player_update: PlayerUpdate) -> Player:
    """Update an existing player."""
    db_player = get_player(db, player_id)

    update_data = player_update.model_dump(exclude_unset=True)

    # Verify team exists if team_id is being updated
    if "team_id" in update_data and update_data["team_id"]:
        team = db.query(Team).filter(Team.id == update_data["team_id"]).first()
        if not team:
            raise TeamNotFoundException(
                f"Team with id {update_data['team_id']} not found"
            )

    for field, value in update_data.items():
        setattr(db_player, field, value)

    db.commit()
    db.refresh(db_player)
    return db_player


def delete_player(db: Session, player_id: int) -> bool:
    """Delete a player."""
    db_player = get_player(db, player_id)
    db.delete(db_player)
    db.commit()
    return True


def get_player_statistics(db: Session, player_id: int) -> dict:
    """Get player statistics including goals, matches played, etc."""
    player = get_player(db, player_id)

    # This would be expanded based on your actual statistics tracking
    return {
        "player_id": player.id,
        "name": player.name,
        "position": player.position,
        "age": player.age,
        "team_id": player.team_id,
        # Add more statistics as your models evolve
        "total_goals": 0,  # Placeholder - would query actual match data
        "matches_played": 0,  # Placeholder - would query actual match data
        "yellow_cards": 0,  # Placeholder
        "red_cards": 0,  # Placeholder
    }


def transfer_player(db: Session, player_id: int, new_team_id: int) -> Player:
    """Transfer a player to a new team."""
    player = get_player(db, player_id)

    # Verify new team exists
    new_team = db.query(Team).filter(Team.id == new_team_id).first()
    if not new_team:
        raise TeamNotFoundException(f"Team with id {new_team_id} not found")

    setattr(player, "team_id", new_team_id)
    db.commit()
    db.refresh(player)
    return player
