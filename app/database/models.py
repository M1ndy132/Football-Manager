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

    __table_args__ = (CheckConstraint("founded_year > 1800", name="chk_founded_year"),)


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
        CheckConstraint("age >= 16 AND age <= 50", name="chk_player_age"),
    )


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    experience_years = Column(Integer, nullable=False)
    specialization = Column(String(100))
    nationality = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("experience_years >= 0", name="chk_coach_experience_years"),
    )


class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    strategy = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("strategy IS NOT NULL", name="chk_manager_strategy"),
    )


class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    built_year = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("capacity > 0", name="chk_venue_capacity"),
        CheckConstraint("built_year > 1800", name="chk_venue_built_year"),
    )


class Referee(Base):
    __tablename__ = "referees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    experience_years = Column(Integer, nullable=False)
    nationality = Column(String(50))
    qualification_level = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("experience_years >= 0", name="chk_referee_experience_years"),
    )


class Sponsor(Base):
    __tablename__ = "sponsors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    industry = Column(String(100))
    sponsorship_amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "sponsorship_amount > 0", name="chk_sponsor_sponsorship_amount"
        ),
    )
