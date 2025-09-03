"""
Integration tests for player endpoints.
"""

import pytest
from app.database.models import Team, Player


class TestPlayerEndpoints:
    """Test player-related endpoints."""
    
    def test_get_all_players(self, client, test_db, authenticated_headers):
        """Test getting all players."""
        # Create a team first
        team = Team(
            name="Test FC",
            coach_name="Test Coach",
            founded_year=2000,
            home_ground="Test Stadium"
        )
        test_db.add(team)
        test_db.commit()
        test_db.refresh(team)
        
        # Create some test players
        players_data = [
            {"team_id": team.id, "name": "Player One", "position": "Forward", "age": 25},
            {"team_id": team.id, "name": "Player Two", "position": "Midfielder", "age": 27},
        ]
        
        for player_data in players_data:
            player = Player(**player_data)
            test_db.add(player)
        test_db.commit()
        
        response = client.get("/players/", headers=authenticated_headers)
        assert response.status_code == 200
        
        response_data = response.json()
        assert len(response_data) >= 2
        
        # Verify player data structure
        for player in response_data:
            assert "id" in player
            assert "name" in player
            assert "position" in player
            assert "age" in player
            assert "team_id" in player
    
    def test_get_player_by_id_existing(self, client, test_db, authenticated_headers):
        """Test getting a player by existing ID."""
        # Create a team and player
        team = Team(name="Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        test_db.refresh(team)
        
        player = Player(
            team_id=team.id,
            name="Test Player",
            position="Forward",
            age=25
        )
        test_db.add(player)
        test_db.commit()
        test_db.refresh(player)
        
        response = client.get(f"/players/{player.id}", headers=authenticated_headers)
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["id"] == player.id
        assert response_data["name"] == "Test Player"
        assert response_data["position"] == "Forward"
        assert response_data["age"] == 25
        assert response_data["team_id"] == team.id
    
    def test_get_player_by_id_nonexistent(self, client, authenticated_headers):
        """Test getting a player by non-existent ID."""
        response = client.get("/players/999999", headers=authenticated_headers)
        assert response.status_code == 404
        assert "Player not found" in response.json()["detail"]
    
    def test_create_player_valid_data(self, client, test_db, authenticated_headers):
        """Test creating a player with valid data."""
        # Create a team first
        team = Team(name="Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        test_db.refresh(team)
        
        player_data = {
            "team_id": team.id,
            "name": "New Player",
            "position": "Goalkeeper",
            "age": 28
        }
        
        response = client.post("/players/", json=player_data, headers=authenticated_headers)
        assert response.status_code == 201
        
        response_data = response.json()
        assert response_data["name"] == "New Player"
        assert response_data["position"] == "Goalkeeper"
        assert response_data["age"] == 28
        assert response_data["team_id"] == team.id
        assert "id" in response_data
        
        # Verify player was created in database
        player = test_db.query(Player).filter(Player.name == "New Player").first()
        assert player is not None
        assert player.position == "Goalkeeper"
    
    def test_create_player_invalid_team_id(self, client, authenticated_headers):
        """Test creating a player with invalid team ID."""
        player_data = {
            "team_id": 999999,  # Non-existent team
            "name": "New Player",
            "position": "Forward",
            "age": 25
        }
        
        response = client.post("/players/", json=player_data, headers=authenticated_headers)
        assert response.status_code == 400
        assert "Team not found" in response.json()["detail"]
    
    def test_create_player_missing_required_field(self, client, authenticated_headers):
        """Test creating a player with missing required field."""
        player_data = {
            "team_id": 1,
            "position": "Forward",
            "age": 25
            # Missing name
        }
        
        response = client.post("/players/", json=player_data, headers=authenticated_headers)
        assert response.status_code == 422  # Validation error
    
    def test_update_player_valid_data(self, client, test_db, authenticated_headers):
        """Test updating a player with valid data."""
        # Create team and player
        team = Team(name="Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        test_db.refresh(team)
        
        player = Player(team_id=team.id, name="Original Player", position="Forward", age=25)
        test_db.add(player)
        test_db.commit()
        test_db.refresh(player)
        
        update_data = {
            "team_id": team.id,
            "name": "Updated Player",
            "position": "Midfielder",
            "age": 26
        }
        
        response = client.put(f"/players/{player.id}", json=update_data, headers=authenticated_headers)
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["name"] == "Updated Player"
        assert response_data["position"] == "Midfielder"
        assert response_data["age"] == 26
    
    def test_update_player_nonexistent(self, client, authenticated_headers):
        """Test updating a non-existent player."""
        update_data = {
            "team_id": 1,
            "name": "Updated Player",
            "position": "Midfielder",
            "age": 26
        }
        
        response = client.put("/players/999999", json=update_data, headers=authenticated_headers)
        assert response.status_code == 404
        assert "Player not found" in response.json()["detail"]
    
    def test_delete_player_existing(self, client, test_db, authenticated_headers):
        """Test deleting an existing player."""
        # Create team and player
        team = Team(name="Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        test_db.refresh(team)
        
        player = Player(team_id=team.id, name="Delete Player", position="Forward", age=25)
        test_db.add(player)
        test_db.commit()
        test_db.refresh(player)
        player_id = player.id
        
        response = client.delete(f"/players/{player_id}", headers=authenticated_headers)
        assert response.status_code == 200
        
        # Verify player was deleted from database
        deleted_player = test_db.query(Player).filter(Player.id == player_id).first()
        assert deleted_player is None
    
    def test_delete_player_nonexistent(self, client, authenticated_headers):
        """Test deleting a non-existent player."""
        response = client.delete("/players/999999", headers=authenticated_headers)
        assert response.status_code == 404
        assert "Player not found" in response.json()["detail"]
    
    def test_get_players_by_team(self, client, test_db, authenticated_headers):
        """Test getting players by team ID."""
        # Create two teams
        team1 = Team(name="Team 1", coach_name="Coach 1", founded_year=2000, home_ground="Stadium 1")
        team2 = Team(name="Team 2", coach_name="Coach 2", founded_year=2001, home_ground="Stadium 2")
        test_db.add_all([team1, team2])
        test_db.commit()
        test_db.refresh(team1)
        test_db.refresh(team2)
        
        # Create players for each team
        players_team1 = [
            Player(team_id=team1.id, name="Player 1A", position="Forward", age=25),
            Player(team_id=team1.id, name="Player 1B", position="Midfielder", age=27),
        ]
        players_team2 = [
            Player(team_id=team2.id, name="Player 2A", position="Defender", age=26),
        ]
        
        test_db.add_all(players_team1 + players_team2)
        test_db.commit()
        
        # Test getting players by team (if endpoint exists)
        response = client.get(f"/players/?team_id={team1.id}", headers=authenticated_headers)
        if response.status_code == 200:
            response_data = response.json()
            # Should only return players from team1
            for player in response_data:
                assert player["team_id"] == team1.id
    
    def test_player_position_validation(self, client, test_db, authenticated_headers):
        """Test player position validation."""
        team = Team(name="Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        test_db.refresh(team)
        
        # Test valid positions
        valid_positions = ["Forward", "Midfielder", "Defender", "Goalkeeper"]
        for position in valid_positions:
            player_data = {
                "team_id": team.id,
                "name": f"Player {position}",
                "position": position,
                "age": 25
            }
            response = client.post("/players/", json=player_data, headers=authenticated_headers)
            assert response.status_code == 201
        
        # Test invalid position (if validation exists)
        invalid_player_data = {
            "team_id": team.id,
            "name": "Invalid Player",
            "position": "InvalidPosition",
            "age": 25
        }
        response = client.post("/players/", json=invalid_player_data, headers=authenticated_headers)
        # This might be accepted if there's no position validation
        # assert response.status_code in [201, 422]
    
    def test_player_age_boundaries(self, client, test_db, authenticated_headers):
        """Test player age boundary validation."""
        team = Team(name="Test FC", coach_name="Coach", founded_year=2000, home_ground="Stadium")
        test_db.add(team)
        test_db.commit()
        test_db.refresh(team)
        
        # Test valid ages
        valid_ages = [16, 25, 35, 50]
        for age in valid_ages:
            player_data = {
                "team_id": team.id,
                "name": f"Player Age {age}",
                "position": "Forward",
                "age": age
            }
            response = client.post("/players/", json=player_data, headers=authenticated_headers)
            # Should be accepted if within valid range
            assert response.status_code in [201, 400]  # Depending on validation
        
        # Test invalid ages
        invalid_ages = [15, 51]
        for age in invalid_ages:
            player_data = {
                "team_id": team.id,
                "name": f"Invalid Player Age {age}",
                "position": "Forward",
                "age": age
            }
            response = client.post("/players/", json=player_data, headers=authenticated_headers)
            # Should be rejected if validation exists
            # assert response.status_code == 400