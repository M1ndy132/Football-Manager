from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    coach_name = Column(String(100))
    founded_year = Column(Integer)
    home_ground = Column(String(150))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("founded_year > 1800", name="chk_founded_year"),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    team_a_id = Column(Integer, nullable=False)
    team_b_id = Column(Integer, nullable=False)
    match_date = Column(DateTime, nullable=False)
    venue = Column(String(150), nullable=False)
    score_team_a = Column(Integer, default=0)
    score_team_b = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("score_team_a >= 0", name="chk_score_team_a"),
        CheckConstraint("score_team_b >= 0", name="chk_score_team_b"),
    )       

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    position = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)   
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("age > 0", name="chk_player_age"),
    )   
    


