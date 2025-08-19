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