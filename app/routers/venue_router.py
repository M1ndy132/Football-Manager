# app/routers/venue_router.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.models import Venue
from app.database.session import get_db
from app.schemas.venue import VenueCreate, VenueResponse, VenueUpdate

router = APIRouter(prefix="/venues", tags=["venues"])


@router.post("/", response_model=VenueResponse, status_code=status.HTTP_201_CREATED)
def create_venue(venue: VenueCreate, db: Session = Depends(get_db)):
    # Check if venue with same name already exists
    existing_venue = db.query(Venue).filter(Venue.name == venue.name).first()
    if existing_venue:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Venue with this name already exists",
        )

    db_venue = Venue(**venue.dict())
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue


@router.get("/", response_model=List[VenueResponse])
def get_venues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    venues = db.query(Venue).offset(skip).limit(limit).all()
    return venues


@router.get("/{venue_id}", response_model=VenueResponse)
def get_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found"
        )
    return venue


@router.get("/city/{city_name}", response_model=List[VenueResponse])
def get_venues_by_city(city_name: str, db: Session = Depends(get_db)):
    venues = db.query(Venue).filter(Venue.city.ilike(f"%{city_name}%")).all()
    return venues


@router.put("/{venue_id}", response_model=VenueResponse)
def update_venue(
    venue_id: int, venue_update: VenueUpdate, db: Session = Depends(get_db)
):
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found"
        )

    for field, value in venue_update.dict(exclude_unset=True).items():
        setattr(venue, field, value)

    db.commit()
    db.refresh(venue)
    return venue


@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venue(venue_id: int, db: Session = Depends(get_db)):
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found"
        )

    db.delete(venue)
    db.commit()
    return None
