# app/schemas/team.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TeamBase(BaseModel):
    name: str = Field(..., max_length=100)
    coach_name: Optional[str] = Field(None, max_length=100)
    founded_year: Optional[int] = Field(None, gt=1800)
    home_ground: Optional[str] = Field(None, max_length=150)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    coach_name: Optional[str] = Field(None, max_length=100)
    founded_year: Optional[int] = Field(None, gt=1800)
    home_ground: Optional[str] = Field(None, max_length=150)


class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
