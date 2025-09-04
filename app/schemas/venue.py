# app/schemas/venue.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VenueBase(BaseModel):
    name: str = Field(..., max_length=150)
    city: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)
    capacity: int = Field(..., ge=0)
    built_year: Optional[int] = Field(None, gt=1800)

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    capacity: Optional[int] = Field(None, ge=0)
    built_year: Optional[int] = Field(None, gt=1800)

class VenueResponse(VenueBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
