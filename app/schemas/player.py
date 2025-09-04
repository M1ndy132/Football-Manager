# app/schemas/player.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PlayerBase(BaseModel):
    team_id: int
    name: str = Field(..., max_length=100)
    position: str = Field(..., max_length=50)
    age: int = Field(..., gt=0)


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=50)
    age: Optional[int] = Field(None, gt=0)


class PlayerResponse(PlayerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
