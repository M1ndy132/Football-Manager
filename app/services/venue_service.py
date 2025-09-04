"""
Venue service for Football League Manager.

Contains business logic for venue management, including
CRUD operations and venue scheduling.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.models import Venue, Match
from app.schemas.venue import VenueCreate, VenueUpdate
from app.core.exceptions import VenueNotFoundException, DuplicateResourceException


def get_venue(db: Session, venue_id: int) -> Venue:
    """Get a venue by ID."""
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise VenueNotFoundException(f"Venue with id {venue_id} not found")
    return venue


def get_venue_by_name(db: Session, name: str) -> Optional[Venue]:
    """Get a venue by name."""
    return db.query(Venue).filter(Venue.name == name).first()


def get_venues(db: Session, skip: int = 0, limit: int = 100) -> List[Venue]:
    """Get all venues with pagination."""
    return db.query(Venue).offset(skip).limit(limit).all()


def create_venue(db: Session, venue: VenueCreate) -> Venue:
    """Create a new venue."""
    # Check if venue with same name already exists
    existing_venue = get_venue_by_name(db, venue.name)
    if existing_venue:
        raise DuplicateResourceException(f"Venue with name '{venue.name}' already exists")
    
    db_venue = Venue(**venue.model_dump())
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue


def update_venue(db: Session, venue_id: int, venue_update: VenueUpdate) -> Venue:
    """Update an existing venue."""
    db_venue = get_venue(db, venue_id)
    
    update_data = venue_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_venue, field, value)
    
    db.commit()
    db.refresh(db_venue)
    return db_venue


def delete_venue(db: Session, venue_id: int) -> bool:
    """Delete a venue."""
    db_venue = get_venue(db, venue_id)
    db.delete(db_venue)
    db.commit()
    return True


def get_venues_by_city(db: Session, city: str) -> List[Venue]:
    """Get venues by city."""
    return db.query(Venue).filter(Venue.city == city).all()


def get_venues_by_capacity_range(db: Session, min_capacity: int, max_capacity: int) -> List[Venue]:
    """Get venues within capacity range."""
    return db.query(Venue).filter(
        Venue.capacity >= min_capacity,
        Venue.capacity <= max_capacity
    ).all()


def get_venue_matches(db: Session, venue_id: int) -> List[Match]:
    """Get all matches scheduled at a venue."""
    venue = get_venue(db, venue_id)
    return db.query(Match).filter(Match.venue == venue.name).all()


def get_venue_statistics(db: Session, venue_id: int) -> dict:
    """Get venue statistics and details."""
    venue = get_venue(db, venue_id)
    matches = get_venue_matches(db, venue_id)
    
    return {
        "venue_id": venue.id,
        "name": venue.name,
        "city": venue.city,
        "capacity": venue.capacity,
        "built_year": venue.built_year,
        "total_matches": len(matches),
        # Additional statistics would go here
        "average_attendance": None,  # Placeholder
        "total_attendance": None,  # Placeholder
    }

