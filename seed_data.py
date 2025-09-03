#!/usr/bin/env python3
"""
Seed Data Script for Football League Manager
Populates the database with realistic demo data for presentations and testing.
"""

import asyncio
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, Team, User, Match, Player, Coach, Manager, Venue, Referee, Sponsor
from app.core.security import get_password_hash

# Database configuration
DATABASE_URL = "sqlite:///./football.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

def seed_users():
    """Create demo users"""
    db = SessionLocal()
    try:
        users_data = [
            {"username": "admin", "email": "admin@footballmanager.com", "full_name": "League Administrator", "password": "admin123"},
            {"username": "manager1", "email": "manager1@team.com", "full_name": "Team Manager One", "password": "manager123"},
            {"username": "manager2", "email": "manager2@team.com", "full_name": "Team Manager Two", "password": "manager123"},
            {"username": "coach1", "email": "coach1@team.com", "full_name": "Head Coach Smith", "password": "coach123"},
            {"username": "referee1", "email": "referee1@league.com", "full_name": "Chief Referee Johnson", "password": "ref123"},
        ]
        
        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"])
            )
            db.add(user)
        
        db.commit()
        print("✅ Users seeded successfully")
    except Exception as e:
        print(f"❌ Error seeding users: {e}")
        db.rollback()
    finally:
        db.close()

def seed_venues():
    """Create demo venues"""
    db = SessionLocal()
    try:
        venues_data = [
            {"name": "Wembley Stadium", "city": "London", "country": "England", "capacity": 90000, "built_year": 2007},
            {"name": "Old Trafford", "city": "Manchester", "country": "England", "capacity": 74879, "built_year": 1910},
            {"name": "Emirates Stadium", "city": "London", "country": "England", "capacity": 60704, "built_year": 2006},
            {"name": "Anfield", "city": "Liverpool", "country": "England", "capacity": 53394, "built_year": 1884},
            {"name": "Etihad Stadium", "city": "Manchester", "country": "England", "capacity": 55017, "built_year": 2002},
            {"name": "Community Sports Ground", "city": "Local Town", "country": "England", "capacity": 5000, "built_year": 1995},
        ]
        
        for venue_data in venues_data:
            venue = Venue(**venue_data)
            db.add(venue)
        
        db.commit()
        print("✅ Venues seeded successfully")
    except Exception as e:
        print(f"❌ Error seeding venues: {e}")
        db.rollback()
    finally:
        db.close()

def seed_teams():
    """Create demo teams"""
    db = SessionLocal()
    try:
        teams_data = [
            {"name": "Manchester United", "coach_name": "Erik ten Hag", "founded_year": 1878, "home_ground": "Old Trafford"},
            {"name": "Arsenal FC", "coach_name": "Mikel Arteta", "founded_year": 1886, "home_ground": "Emirates Stadium"},
            {"name": "Liverpool FC", "coach_name": "Jürgen Klopp", "founded_year": 1892, "home_ground": "Anfield"},
            {"name": "Manchester City", "coach_name": "Pep Guardiola", "founded_year": 1880, "home_ground": "Etihad Stadium"},
            {"name": "Chelsea FC", "coach_name": "Mauricio Pochettino", "founded_year": 1905, "home_ground": "Stamford Bridge"},
            {"name": "Tottenham Hotspur", "coach_name": "Ange Postecoglou", "founded_year": 1882, "home_ground": "Tottenham Hotspur Stadium"},
            {"name": "Newcastle United", "coach_name": "Eddie Howe", "founded_year": 1892, "home_ground": "St. James' Park"},
            {"name": "Brighton & Hove Albion", "coach_name": "Roberto De Zerbi", "founded_year": 1901, "home_ground": "Amex Stadium"},
        ]
        
        for team_data in teams_data:
            team = Team(**team_data)
            db.add(team)
        
        db.commit()
        print("✅ Teams seeded successfully")
    except Exception as e:
        print(f"❌ Error seeding teams: {e}")
        db.rollback()
    finally:
        db.close()

def seed_players():
    """Create demo players"""
    db = SessionLocal()
    try:
        # Get team IDs first
        teams = db.query(Team).all()
        
        players_data = [
            # Manchester United (Team ID 1)
            {"team_id": 1, "name": "Marcus Rashford", "position": "Forward", "age": 26},
            {"team_id": 1, "name": "Bruno Fernandes", "position": "Midfielder", "age": 29},
            {"team_id": 1, "name": "Harry Maguire", "position": "Defender", "age": 30},
            {"team_id": 1, "name": "André Onana", "position": "Goalkeeper", "age": 27},
            
            # Arsenal FC (Team ID 2)
            {"team_id": 2, "name": "Bukayo Saka", "position": "Forward", "age": 22},
            {"team_id": 2, "name": "Martin Ødegaard", "position": "Midfielder", "age": 24},
            {"team_id": 2, "name": "William Saliba", "position": "Defender", "age": 22},
            {"team_id": 2, "name": "Aaron Ramsdale", "position": "Goalkeeper", "age": 25},
            
            # Liverpool FC (Team ID 3)
            {"team_id": 3, "name": "Mohamed Salah", "position": "Forward", "age": 31},
            {"team_id": 3, "name": "Jordan Henderson", "position": "Midfielder", "age": 33},
            {"team_id": 3, "name": "Virgil van Dijk", "position": "Defender", "age": 32},
            {"team_id": 3, "name": "Alisson Becker", "position": "Goalkeeper", "age": 30},
            
            # Manchester City (Team ID 4)
            {"team_id": 4, "name": "Erling Haaland", "position": "Forward", "age": 23},
            {"team_id": 4, "name": "Kevin De Bruyne", "position": "Midfielder", "age": 32},
            {"team_id": 4, "name": "Ruben Dias", "position": "Defender", "age": 26},
            {"team_id": 4, "name": "Ederson", "position": "Goalkeeper", "age": 29},
            
            # Chelsea FC (Team ID 5)
            {"team_id": 5, "name": "Raheem Sterling", "position": "Forward", "age": 28},
            {"team_id": 5, "name": "Enzo Fernández", "position": "Midfielder", "age": 22},
            {"team_id": 5, "name": "Thiago Silva", "position": "Defender", "age": 39},
            {"team_id": 5, "name": "Kepa Arrizabalaga", "position": "Goalkeeper", "age": 28},
        ]
        
        for player_data in players_data:
            player = Player(**player_data)
            db.add(player)
        
        db.commit()
        print("✅ Players seeded successfully")
    except Exception as e:
        print(f"❌ Error seeding players: {e}")
        db.rollback()
    finally:
        db.close()

def seed_coaches():
    """Create demo coaches"""
    db = SessionLocal()
    try:
        coaches_data = [
            {"team_id": 1, "name": "Erik ten Hag", "experience_years": 15, "specialization": "Tactical Innovation", "nationality": "Dutch"},
            {"team_id": 2, "name": "Mikel Arteta", "experience_years": 8, "specialization": "Youth Development", "nationality": "Spanish"},
            {"team_id": 3, "name": "Jürgen Klopp", "experience_years": 20, "specialization": "High-Intensity Football", "nationality": "German"},
            {"team_id": 4, "name": "Pep Guardiola", "experience_years": 18, "specialization": "Possession Football", "nationality": "Spanish"},
            {"team_id": 5, "name": "Mauricio Pochettino", "experience_years": 16, "specialization": "Player Development", "nationality": "Argentine"},
        ]
        
        for coach_data in coaches_data:
            coach = Coach(**coach_data)
            db.add(coach)
        
        db.commit()
        print("✅ Coaches seeded successfully")
    except Exception as e:
        print(f"❌ Error seeding coaches: {e}")
        db.rollback()
    finally:
        db.close()

def seed_referees():
    """Create demo referees"""
    db = SessionLocal()
    try:
        referees_data = [
            {"name": "Michael Oliver", "experience_years": 15, "nationality": "English", "qualification_level": "FIFA International"},
            {"name": "Anthony Taylor", "experience_years": 12, "nationality": "English", "qualification_level": "Premier League"},
            {"name": "Chris Kavanagh", "experience_years": 8, "nationality": "English", "qualification_level": "Premier League"},
            {"name": "Craig Pawson", "experience_years": 10, "nationality": "English", "qualification_level": "Premier League"},
            {"name": "Simon Hooper", "experience_years": 7, "nationality": "English", "qualification_level": "Championship"},
        ]
        
        for referee_data in referees_data:
            referee = Referee(**referee_data)
            db.add(referee)
        
        db.commit()
        print("✅ Referees seeded successfully")
    except Exception as e:
        print(f"❌ Error seeding referees: {e}")
        db.rollback()
    finally:
        db.close()

def seed_matches():
    """Create demo matches with realistic scores"""
    db = SessionLocal()
    try:
        # Create matches for the past few weeks and upcoming matches
        base_date = datetime.now() - timedelta(days=30)
        
        matches_data = [
            # Past matches with scores
            {"team_a_id": 1, "team_b_id": 2, "match_date": base_date + timedelta(days=1), "venue": "Old Trafford", "score_team_a": 2, "score_team_b": 1},
            {"team_a_id": 3, "team_b_id": 4, "match_date": base_date + timedelta(days=2), "venue": "Anfield", "score_team_a": 1, "score_team_b": 3},
            {"team_a_id": 5, "team_b_id": 6, "match_date": base_date + timedelta(days=3), "venue": "Stamford Bridge", "score_team_a": 0, "score_team_b": 2},
            {"team_a_id": 2, "team_b_id": 3, "match_date": base_date + timedelta(days=7), "venue": "Emirates Stadium", "score_team_a": 3, "score_team_b": 1},
            {"team_a_id": 4, "team_b_id": 1, "match_date": base_date + timedelta(days=8), "venue": "Etihad Stadium", "score_team_a": 1, "score_team_b": 1},
            {"team_a_id": 6, "team_b_id": 7, "match_date": base_date + timedelta(days=9), "venue": "Tottenham Hotspur Stadium", "score_team_a": 2, "score_team_b": 0},
            
            # Upcoming matches (no scores)
            {"team_a_id": 1, "team_b_id": 3, "match_date": datetime.now() + timedelta(days=3), "venue": "Old Trafford", "score_team_a": 0, "score_team_b": 0},
            {"team_a_id": 2, "team_b_id": 4, "match_date": datetime.now() + timedelta(days=5), "venue": "Emirates Stadium", "score_team_a": 0, "score_team_b": 0},
            {"team_a_id": 5, "team_b_id": 7, "match_date": datetime.now() + timedelta(days=7), "venue": "Stamford Bridge", "score_team_a": 0, "score_team_b": 0},
            {"team_a_id": 6, "team_b_id": 8, "match_date": datetime.now() + timedelta(days=10), "venue": "Tottenham Hotspur Stadium", "score_team_a": 0, "score_team_b": 0},
        ]
        
        for match_data in matches_data:
            match = Match(**match_data)
            db.add(match)
        
        db.commit()
        print("✅ Matches seeded successfully")
    except Exception as e:
        print(f"❌ Error seeding matches: {e}")
        db.rollback()
    finally:
        db.close()

def seed_sponsors():
    """Create demo sponsors"""
    db = SessionLocal()
    try:
        sponsors_data = [
            {"name": "Nike", "industry": "Sports Apparel", "sponsorship_amount": 500000},
            {"name": "Adidas", "industry": "Sports Apparel", "sponsorship_amount": 450000},
            {"name": "Emirates Airlines", "industry": "Aviation", "sponsorship_amount": 600000},
            {"name": "Etihad Airways", "industry": "Aviation", "sponsorship_amount": 550000},
            {"name": "TeamViewer", "industry": "Technology", "sponsorship_amount": 400000},
            {"name": "Chevrolet", "industry": "Automotive", "sponsorship_amount": 350000},
        ]
        
        for sponsor_data in sponsors_data:
            sponsor = Sponsor(**sponsor_data)
            db.add(sponsor)
        
        db.commit()
        print("✅ Sponsors seeded successfully")
    except Exception as e:
        print(f"❌ Error seeding sponsors: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Run all seed functions"""
    print("🌱 Starting database seeding...")
    
    # Create tables first
    create_tables()
    
    # Seed data in correct order (considering foreign key relationships)
    seed_users()
    seed_venues()
    seed_teams()
    seed_players()
    seed_coaches()
    seed_referees()
    seed_matches()
    seed_sponsors()
    
    print("🎉 Database seeding completed successfully!")
    print("\n📊 Demo Data Summary:")
    print("- 5 Users (admin, managers, coaches, referee)")
    print("- 8 Premier League Teams")
    print("- 20+ Players across teams")
    print("- 5 Experienced Coaches")
    print("- 5 Professional Referees")
    print("- 10 Matches (6 completed, 4 upcoming)")
    print("- 6 Venue locations")
    print("- 6 Major sponsors")
    print("\n🚀 You can now demo your API with realistic data!")
    print("👉 Visit: http://127.0.0.1:8000/demo")

if __name__ == "__main__":
    main()
