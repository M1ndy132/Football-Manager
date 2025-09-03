"""
Unit tests for database models.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from app.database.models import Team, User, Player, Coach, Match, Venue, Referee, Sponsor, Manager
from app.core.security import get_password_hash


def assert_equal(actual, expected):
    """Helper function to safely compare SQLAlchemy model attributes."""
    if hasattr(actual, 'proxy_set'):
        # This is a SQLAlchemy instrumented attribute, get the actual value
        actual_value = getattr(actual, '_sa_instance_state').attrs.get(actual.key).value
        assert actual_value == expected
    else:
        assert actual == expected


class TestTeamModel:
    """Test Team model."""
    
    def test_create_team_valid_data(self, test_db):
        """Test creating a team with valid data."""
        team = Team(
            name="Test FC",
            coach_name="Test Coach",
            founded_year=2000,
            home_ground="Test Stadium"
        )
        test_db.add(team)
        test_db.commit()
        test_db.refresh(team)  # Refresh to ensure values are loaded
        
        # Use getattr or direct access with proper typing
        assert team.id is not None
        assert getattr(team, 'name') == "Test FC"
        assert getattr(team, 'coach_name') == "Test Coach"
        assert getattr(team, 'founded_year') == 2000
        assert getattr(team, 'home_ground') == "Test Stadium"
        assert team.created_at is not None
    
    def test_team_name_unique_constraint(self, test_db):
        """Test that team names must be unique."""
        team1 = Team(name="Unique FC 1", coach_name="Coach 1", founded_year=2000, home_ground="Stadium 1")
        team2 = Team(name="Unique FC 1", coach_name="Coach 2", founded_year=2001, home_ground="Stadium 2")
        
        test_db.add(team1)
        test_db.commit()
        
        test_db.add(team2)
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_team_founded_year_constraint(self, test_db):
        """Test founded year constraint (must be >= 1850)."""
        team = Team(
            name="Old FC",
            coach_name="Old Coach",
            founded_year=1800,  # Invalid year
            home_ground="Old Stadium"
        )
        test_db.add(team)
        with pytest.raises(IntegrityError):
            test_db.commit()


class TestUserModel:
    """Test User model."""
    
    def test_create_user_valid_data(self, test_db):
        """Test creating a user with valid data."""
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("password123")
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        assert user.id is not None
        assert getattr(user, 'username') == "testuser"
        assert getattr(user, 'email') == "test@example.com"
        assert getattr(user, 'full_name') == "Test User"
        assert getattr(user, 'hashed_password') != "password123"  # Should be hashed
        assert user.created_at is not None
    
    def test_user_username_unique_constraint(self, test_db):
        """Test that usernames must be unique."""
        user1 = User(username="testuser", email="test1@example.com", full_name="User 1", hashed_password="hash1")
        user2 = User(username="testuser", email="test2@example.com", full_name="User 2", hashed_password="hash2")
        
        test_db.add(user1)
        test_db.commit()
        
        test_db.add(user2)
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_user_email_unique_constraint(self, test_db):
        """Test that emails must be unique."""
        user1 = User(username="user1", email="test@example.com", full_name="User 1", hashed_password="hash1")
        user2 = User(username="user2", email="test@example.com", full_name="User 2", hashed_password="hash2")
        
        test_db.add(user1)
        test_db.commit()
        
        test_db.add(user2)
        with pytest.raises(IntegrityError):
            test_db.commit()


class TestPlayerModel:
    """Test Player model."""
    
    def test_create_player_valid_data(self, test_db):
        """Test creating a player with valid data."""
        # Create team first
        team = Team(name="Player Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        
        player = Player(
            team_id=team.id,
            name="Test Player",
            position="Forward",
            age=25
        )
        test_db.add(player)
        test_db.commit()
        test_db.refresh(player)
        
        assert player.id is not None
        assert getattr(player, 'team_id') == team.id
        assert getattr(player, 'name') == "Test Player"
        assert getattr(player, 'position') == "Forward"
        assert getattr(player, 'age') == 25
    
    def test_player_age_constraint(self, test_db):
        """Test player age constraint (16-50)."""
        team = Team(name="Player Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        team_id = team.id
        
        # Test age too young
        young_player = Player(team_id=team_id, name="Too Young", position="Forward", age=15)
        test_db.add(young_player)
        with pytest.raises(IntegrityError):
            test_db.commit()
        
        test_db.rollback()
        
        # Test age too old  
        old_player = Player(team_id=team_id, name="Too Old", position="Forward", age=51)
        test_db.add(old_player)
        with pytest.raises(IntegrityError):
            test_db.commit()


class TestVenueModel:
    """Test Venue model."""
    
    def test_create_venue_valid_data(self, test_db):
        """Test creating a venue with valid data."""
        venue = Venue(
            name="Test Stadium",
            city="Test City",
            country="Test Country",
            capacity=50000,
            built_year=2010
        )
        test_db.add(venue)
        test_db.commit()
        
        assert venue.id is not None
        assert getattr(venue, 'name') == "Test Stadium"
        assert getattr(venue, 'city') == "Test City"
        assert getattr(venue, 'country') == "Test Country"
        assert getattr(venue, 'capacity') == 50000
        assert getattr(venue, 'built_year') == 2010
    
    def test_venue_capacity_constraint(self, test_db):
        """Test venue capacity constraint (must be > 0)."""
        venue = Venue(
            name="Invalid Stadium",
            city="Test City",
            country="Test Country",
            capacity=0,  # Invalid capacity
            built_year=2010
        )
        test_db.add(venue)
        with pytest.raises(IntegrityError):
            test_db.commit()


class TestMatchModel:
    """Test Match model."""
    
    def test_create_match_valid_data(self, test_db):
        """Test creating a match with valid data."""
        # Create teams first
        team_a = Team(name="Match Team A", coach_name="Coach A", founded_year=2000, home_ground="Stadium A")
        team_b = Team(name="Match Team B", coach_name="Coach B", founded_year=2001, home_ground="Stadium B")
        test_db.add_all([team_a, team_b])
        test_db.commit()
        
        match = Match(
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            match_date=datetime.now() + timedelta(days=7),
            venue="Test Stadium",
            score_team_a=2,
            score_team_b=1
        )
        test_db.add(match)
        test_db.commit()
        
        assert match.id is not None
        assert getattr(match, 'team_a_id') == team_a.id
        assert getattr(match, 'team_b_id') == team_b.id
        assert getattr(match, 'venue') == "Test Stadium"
        assert getattr(match, 'score_team_a') == 2
        assert getattr(match, 'score_team_b') == 1
    
    def test_match_score_constraint(self, test_db):
        """Test match score constraint (must be >= 0)."""
        team_a = Team(name="Match Team A", coach_name="Coach A", founded_year=2000, home_ground="Stadium A")
        team_b = Team(name="Match Team B", coach_name="Coach B", founded_year=2001, home_ground="Stadium B")
        test_db.add_all([team_a, team_b])
        test_db.commit()
        
        match = Match(
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            match_date=datetime.now() + timedelta(days=7),
            venue="Test Stadium",
            score_team_a=-1,  # Invalid score
            score_team_b=0
        )
        test_db.add(match)
        with pytest.raises(IntegrityError):
            test_db.commit()


class TestCoachModel:
    """Test Coach model."""
    
    def test_create_coach_valid_data(self, test_db):
        """Test creating a coach with valid data."""
        team = Team(name="Coach Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        
        coach = Coach(
            team_id=team.id,
            name="Test Coach",
            experience_years=10,
            specialization="Tactics",
            nationality="English"
        )
        test_db.add(coach)
        test_db.commit()
        
        assert coach.id is not None
        assert getattr(coach, 'team_id') == team.id
        assert getattr(coach, 'name') == "Test Coach"
        assert getattr(coach, 'experience_years') == 10
        assert getattr(coach, 'specialization') == "Tactics"
        assert getattr(coach, 'nationality') == "English"
    
    def test_coach_experience_constraint(self, test_db):
        """Test coach experience constraint (must be >= 0)."""
        team = Team(name="Coach Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        
        coach = Coach(
            team_id=team.id,
            name="Invalid Coach",
            experience_years=-1,  # Invalid experience
            specialization="Tactics",
            nationality="English"
        )
        test_db.add(coach)
        with pytest.raises(IntegrityError):
            test_db.commit()


class TestRefereeModel:
    """Test Referee model."""
    
    def test_create_referee_valid_data(self, test_db):
        """Test creating a referee with valid data."""
        referee = Referee(
            name="Test Referee",
            experience_years=5,
            nationality="English",
            qualification_level="Premier League"
        )
        test_db.add(referee)
        test_db.commit()
        
        assert referee.id is not None
        assert getattr(referee, 'name') == "Test Referee"
        assert getattr(referee, 'experience_years') == 5
        assert getattr(referee, 'nationality') == "English"
        assert getattr(referee, 'qualification_level') == "Premier League"


class TestSponsorModel:
    """Test Sponsor model."""
    
    def test_create_sponsor_valid_data(self, test_db):
        """Test creating a sponsor with valid data."""
        sponsor = Sponsor(
            name="Test Sponsor",
            industry="Technology",
            sponsorship_amount=100000
        )
        test_db.add(sponsor)
        test_db.commit()
        
        assert sponsor.id is not None
        assert getattr(sponsor, 'name') == "Test Sponsor"
        assert getattr(sponsor, 'industry') == "Technology"
        assert getattr(sponsor, 'sponsorship_amount') == 100000
    
    def test_sponsor_amount_constraint(self, test_db):
        """Test sponsor amount constraint (must be > 0)."""
        sponsor = Sponsor(
            name="Invalid Sponsor",
            industry="Technology",
            sponsorship_amount=0  # Invalid amount
        )
        test_db.add(sponsor)
        with pytest.raises(IntegrityError):
            test_db.commit()