# app/schemas/match.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MatchBase(BaseModel):
    team_a_id: int
    team_b_id: int
    match_date: datetime
    venue: str = Field(..., max_length=150)
    score_team_a: Optional[int] = Field(0, ge=0)
    score_team_b: Optional[int] = Field(0, ge=0)


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    score_team_a: Optional[int] = Field(None, ge=0)
    score_team_b: Optional[int] = Field(None, ge=0)
    venue: Optional[str] = Field(None, max_length=150)


class MatchResponse(MatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
