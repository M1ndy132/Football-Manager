# app/schemas/coach.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CoachBase(BaseModel):
    team_id: int
    name: str = Field(..., max_length=100)
    experience_years: int = Field(..., ge=0)
    specialization: Optional[str] = Field(None, max_length=100)
    nationality: Optional[str] = Field(None, max_length=50)


class CoachCreate(CoachBase):
    pass


class CoachUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    experience_years: Optional[int] = Field(None, ge=0)
    specialization: Optional[str] = Field(None, max_length=100)
    nationality: Optional[str] = Field(None, max_length=50)


class CoachResponse(CoachBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
