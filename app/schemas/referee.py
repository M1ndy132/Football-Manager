# app/schemas/referee.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RefereeBase(BaseModel):
    name: str = Field(..., max_length=100)
    experience_years: int = Field(..., ge=0)
    nationality: str = Field(..., max_length=50)
    qualification_level: Optional[str] = Field(None, max_length=50)


class RefereeCreate(RefereeBase):
    pass


class RefereeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    experience_years: Optional[int] = Field(None, ge=0)
    nationality: Optional[str] = Field(None, max_length=50)
    qualification_level: Optional[str] = Field(None, max_length=50)


class RefereeResponse(RefereeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
