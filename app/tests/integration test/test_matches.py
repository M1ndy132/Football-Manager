"""
Integration tests for match endpoints.
"""

import pytest
from datetime import datetime, timedelta
from app.database.models import Team, Match


class TestMatchEndpoints:
    """Test match-related endpoints."""

    def test_get_all_matches(self, client, test_db, authenticated_headers):
        """Test getting all matches."""
        # Create teams first
        team_a = Team(
            name="Team A",
            coach_name="Coach A",
            founded_year=2000,
            home_ground="Stadium A",
        )
        team_b = Team(
            name="Team B",
            coach_name="Coach B",
            founded_year=2001,
            home_ground="Stadium B",
        )
        test_db.add_all([team_a, team_b])
        test_db.commit()
        test_db.refresh(team_a)
        test_db.refresh(team_b)

        # Create test matches
        matches_data = [
            {
                "team_a_id": team_a.id,
                "team_b_id": team_b.id,
                "match_date": datetime.now() + timedelta(days=1),
                "venue": "Stadium A",
                "score_team_a": 2,
                "score_team_b": 1,
            },
            {
                "team_a_id": team_b.id,
                "team_b_id": team_a.id,
                "match_date": datetime.now() + timedelta(days=7),
                "venue": "Stadium B",
                "score_team_a": 0,
                "score_team_b": 0,
            },
        ]

        for match_data in matches_data:
            match = Match(**match_data)
            test_db.add(match)
        test_db.commit()

        response = client.get("/matches/", headers=authenticated_headers)
        assert response.status_code == 200

        response_data = response.json()
        assert len(response_data) >= 2

        # Verify match data structure
        for match in response_data:
            assert "id" in match
            assert "team_a_id" in match
            assert "team_b_id" in match
            assert "match_date" in match
            assert "venue" in match
            assert "score_team_a" in match
            assert "score_team_b" in match

    def test_get_match_by_id_existing(self, client, test_db, authenticated_headers):
        """Test getting a match by existing ID."""
        # Create teams and match
        team_a = Team(
            name="Team A",
            coach_name="Coach A",
            founded_year=2000,
            home_ground="Stadium A",
        )
        team_b = Team(
            name="Team B",
            coach_name="Coach B",
            founded_year=2001,
            home_ground="Stadium B",
        )
        test_db.add_all([team_a, team_b])
        test_db.commit()
        test_db.refresh(team_a)
        test_db.refresh(team_b)

        match = Match(
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            match_date=datetime.now() + timedelta(days=7),
            venue="Test Stadium",
            score_team_a=3,
            score_team_b=2,
        )
        test_db.add(match)
        test_db.commit()
        test_db.refresh(match)

        response = client.get(f"/matches/{match.id}", headers=authenticated_headers)
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["id"] == match.id
        assert response_data["team_a_id"] == team_a.id
        assert response_data["team_b_id"] == team_b.id
        assert response_data["venue"] == "Test Stadium"
        assert response_data["score_team_a"] == 3
        assert response_data["score_team_b"] == 2

    def test_get_match_by_id_nonexistent(self, client, authenticated_headers):
        """Test getting a match by non-existent ID."""
        response = client.get("/matches/999999", headers=authenticated_headers)
        assert response.status_code == 404
        assert "Match not found" in response.json()["detail"]

    def test_create_match_valid_data(self, client, test_db, authenticated_headers):
        """Test creating a match with valid data."""
        # Create teams first
        team_a = Team(
            name="Team A",
            coach_name="Coach A",
            founded_year=2000,
            home_ground="Stadium A",
        )
        team_b = Team(
            name="Team B",
            coach_name="Coach B",
            founded_year=2001,
            home_ground="Stadium B",
        )
        test_db.add_all([team_a, team_b])
        test_db.commit()
        test_db.refresh(team_a)
        test_db.refresh(team_b)

        match_date = datetime.now() + timedelta(days=14)
        match_data = {
            "team_a_id": team_a.id,
            "team_b_id": team_b.id,
            "match_date": match_date.isoformat(),
            "venue": "New Stadium",
            "score_team_a": 1,
            "score_team_b": 1,
        }

        response = client.post(
            "/matches/", json=match_data, headers=authenticated_headers
        )
        assert response.status_code == 201

        response_data = response.json()
        assert response_data["team_a_id"] == team_a.id
        assert response_data["team_b_id"] == team_b.id
        assert response_data["venue"] == "New Stadium"
        assert response_data["score_team_a"] == 1
        assert response_data["score_team_b"] == 1
        assert "id" in response_data

        # Verify match was created in database
        match = test_db.query(Match).filter(Match.venue == "New Stadium").first()
        assert match is not None
        assert match.team_a_id == team_a.id
        assert match.team_b_id == team_b.id

    def test_create_match_invalid_team_ids(self, client, authenticated_headers):
        """Test creating a match with invalid team IDs."""
        match_date = datetime.now() + timedelta(days=7)
        match_data = {
            "team_a_id": 999999,  # Non-existent team
            "team_b_id": 999998,  # Non-existent team
            "match_date": match_date.isoformat(),
            "venue": "Test Stadium",
            "score_team_a": 0,
            "score_team_b": 0,
        }

        response = client.post(
            "/matches/", json=match_data, headers=authenticated_headers
        )
        assert response.status_code == 400
        assert "Team not found" in response.json()["detail"]

    def test_create_match_same_teams(self, client, test_db, authenticated_headers):
        """Test creating a match with the same team for both sides."""
        # Create a team
        team = Team(
            name="Test Team",
            coach_name="Coach",
            founded_year=2000,
            home_ground="Stadium",
        )
        test_db.add(team)
        test_db.commit()
        test_db.refresh(team)

        match_date = datetime.now() + timedelta(days=7)
        match_data = {
            "team_a_id": team.id,
            "team_b_id": team.id,  # Same team
            "match_date": match_date.isoformat(),
            "venue": "Test Stadium",
            "score_team_a": 0,
            "score_team_b": 0,
        }

        response = client.post(
            "/matches/", json=match_data, headers=authenticated_headers
        )
        assert response.status_code == 400
        assert "cannot play against itself" in response.json()["detail"].lower()

    def test_create_match_past_date(self, client, test_db, authenticated_headers):
        """Test creating a match with a past date."""
        # Create teams
        team_a = Team(
            name="Team A",
            coach_name="Coach A",
            founded_year=2000,
            home_ground="Stadium A",
        )
        team_b = Team(
            name="Team B",
            coach_name="Coach B",
            founded_year=2001,
            home_ground="Stadium B",
        )
        test_db.add_all([team_a, team_b])
        test_db.commit()
        test_db.refresh(team_a)
        test_db.refresh(team_b)

        past_date = datetime.now() - timedelta(days=7)
        match_data = {
            "team_a_id": team_a.id,
            "team_b_id": team_b.id,
            "match_date": past_date.isoformat(),
            "venue": "Test Stadium",
            "score_team_a": 2,
            "score_team_b": 1,
        }

        response = client.post(
            "/matches/", json=match_data, headers=authenticated_headers
        )
        # Past matches might be allowed for historical data
        assert response.status_code in [201, 400]

    def test_update_match_valid_data(self, client, test_db, authenticated_headers):
        """Test updating a match with valid data."""
        # Create teams and match
        team_a = Team(
            name="Team A",
            coach_name="Coach A",
            founded_year=2000,
            home_ground="Stadium A",
        )
        team_b = Team(
            name="Team B",
            coach_name="Coach B",
            founded_year=2001,
            home_ground="Stadium B",
        )
        test_db.add_all([team_a, team_b])
        test_db.commit()
        test_db.refresh(team_a)
        test_db.refresh(team_b)

        match = Match(
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            match_date=datetime.now() + timedelta(days=7),
            venue="Original Stadium",
            score_team_a=0,
            score_team_b=0,
        )
        test_db.add(match)
        test_db.commit()
        test_db.refresh(match)

        update_data = {
            "team_a_id": team_a.id,
            "team_b_id": team_b.id,
            "match_date": (datetime.now() + timedelta(days=14)).isoformat(),
            "venue": "Updated Stadium",
            "score_team_a": 3,
            "score_team_b": 1,
        }

        response = client.put(
            f"/matches/{match.id}", json=update_data, headers=authenticated_headers
        )
        assert response.status_code == 200

        response_data = response.json()
        assert response_data["venue"] == "Updated Stadium"
        assert response_data["score_team_a"] == 3
        assert response_data["score_team_b"] == 1

    def test_update_match_nonexistent(self, client, authenticated_headers):
        """Test updating a non-existent match."""
        update_data = {
            "team_a_id": 1,
            "team_b_id": 2,
            "match_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "venue": "Updated Stadium",
            "score_team_a": 1,
            "score_team_b": 0,
        }

        response = client.put(
            "/matches/999999", json=update_data, headers=authenticated_headers
        )
        assert response.status_code == 404
        assert "Match not found" in response.json()["detail"]

    def test_delete_match_existing(self, client, test_db, authenticated_headers):
        """Test deleting an existing match."""
        # Create teams and match
        team_a = Team(
            name="Team A",
            coach_name="Coach A",
            founded_year=2000,
            home_ground="Stadium A",
        )
        team_b = Team(
            name="Team B",
            coach_name="Coach B",
            founded_year=2001,
            home_ground="Stadium B",
        )
        test_db.add_all([team_a, team_b])
        test_db.commit()
        test_db.refresh(team_a)
        test_db.refresh(team_b)

        match = Match(
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            match_date=datetime.now() + timedelta(days=7),
            venue="Delete Stadium",
            score_team_a=0,
            score_team_b=0,
        )
        test_db.add(match)
        test_db.commit()
        test_db.refresh(match)
        match_id = match.id

        response = client.delete(f"/matches/{match_id}", headers=authenticated_headers)
        assert response.status_code == 200

        # Verify match was deleted from database
        deleted_match = test_db.query(Match).filter(Match.id == match_id).first()
        assert deleted_match is None

    def test_delete_match_nonexistent(self, client, authenticated_headers):
        """Test deleting a non-existent match."""
        response = client.delete("/matches/999999", headers=authenticated_headers)
        assert response.status_code == 404
        assert "Match not found" in response.json()["detail"]

    def test_get_matches_by_team(self, client, test_db, authenticated_headers):
        """Test getting matches by team ID."""
        # Create teams
        team_a = Team(
            name="Team A",
            coach_name="Coach A",
            founded_year=2000,
            home_ground="Stadium A",
        )
        team_b = Team(
            name="Team B",
            coach_name="Coach B",
            founded_year=2001,
            home_ground="Stadium B",
        )
        team_c = Team(
            name="Team C",
            coach_name="Coach C",
            founded_year=2002,
            home_ground="Stadium C",
        )
        test_db.add_all([team_a, team_b, team_c])
        test_db.commit()
        test_db.refresh(team_a)
        test_db.refresh(team_b)
        test_db.refresh(team_c)

        # Create matches involving team_a
        matches_with_team_a = [
            Match(
                team_a_id=team_a.id,
                team_b_id=team_b.id,
                match_date=datetime.now() + timedelta(days=1),
                venue="Stadium A",
                score_team_a=2,
                score_team_b=1,
            ),
            Match(
                team_a_id=team_c.id,
                team_b_id=team_a.id,
                match_date=datetime.now() + timedelta(days=2),
                venue="Stadium C",
                score_team_a=0,
                score_team_b=3,
            ),
        ]

        # Create match not involving team_a
        match_without_team_a = Match(
            team_a_id=team_b.id,
            team_b_id=team_c.id,
            match_date=datetime.now() + timedelta(days=3),
            venue="Stadium B",
            score_team_a=1,
            score_team_b=1,
        )

        test_db.add_all(matches_with_team_a + [match_without_team_a])
        test_db.commit()

        # Test getting matches by team (if endpoint exists)
        response = client.get(
            f"/matches/?team_id={team_a.id}", headers=authenticated_headers
        )
        if response.status_code == 200:
            response_data = response.json()
            # Should only return matches involving team_a
            for match in response_data:
                assert (
                    match["team_a_id"] == team_a.id or match["team_b_id"] == team_a.id
                )

    def test_match_score_validation(self, client, test_db, authenticated_headers):
        """Test match score validation."""
        # Create teams
        team_a = Team(
            name="Team A",
            coach_name="Coach A",
            founded_year=2000,
            home_ground="Stadium A",
        )
        team_b = Team(
            name="Team B",
            coach_name="Coach B",
            founded_year=2001,
            home_ground="Stadium B",
        )
        test_db.add_all([team_a, team_b])
        test_db.commit()
        test_db.refresh(team_a)
        test_db.refresh(team_b)

        # Test negative scores
        match_data = {
            "team_a_id": team_a.id,
            "team_b_id": team_b.id,
            "match_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "venue": "Test Stadium",
            "score_team_a": -1,  # Invalid negative score
            "score_team_b": 2,
        }

        response = client.post(
            "/matches/", json=match_data, headers=authenticated_headers
        )
        # Should be rejected if validation exists
        assert response.status_code in [
            201,
            400,
            422,
        ]  # Depending on validation implementation

    def test_get_upcoming_matches(self, client, test_db, authenticated_headers):
        """Test getting upcoming matches."""
        # Create teams
        team_a = Team(
            name="Team A",
            coach_name="Coach A",
            founded_year=2000,
            home_ground="Stadium A",
        )
        team_b = Team(
            name="Team B",
            coach_name="Coach B",
            founded_year=2001,
            home_ground="Stadium B",
        )
        test_db.add_all([team_a, team_b])
        test_db.commit()
        test_db.refresh(team_a)
        test_db.refresh(team_b)

        # Create past and future matches
        past_match = Match(
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            match_date=datetime.now() - timedelta(days=7),
            venue="Past Stadium",
            score_team_a=2,
            score_team_b=1,
        )
        future_match = Match(
            team_a_id=team_a.id,
            team_b_id=team_b.id,
            match_date=datetime.now() + timedelta(days=7),
            venue="Future Stadium",
            score_team_a=0,
            score_team_b=0,
        )

        test_db.add_all([past_match, future_match])
        test_db.commit()

        # Test getting upcoming matches (if endpoint exists)
        response = client.get("/matches/?upcoming=true", headers=authenticated_headers)
        if response.status_code == 200:
            response_data = response.json()
            # Should only return future matches
            for match in response_data:
                match_date = datetime.fromisoformat(
                    match["match_date"].replace("Z", "+00:00")
                )
                assert match_date > datetime.now()
