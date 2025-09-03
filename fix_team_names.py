#!/usr/bin/env python3
"""
Script to fix test team name conflicts by making them unique.
"""
import re

def fix_team_name_conflicts():
    file_path = r"c:\Users\Amanda\AppData\Local\GitHubDesktop\app-3.5.2\Football-Manager\app\tests\unit test\model.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace duplicate team names with unique versions
    replacements = [
        ('Team(name="Test FC"', 'Team(name="Player Test FC"'),  # For player tests
        ('Team(name="Team A"', 'Team(name="Match Team A"'),     # For match tests
        ('Team(name="Team B"', 'Team(name="Match Team B"'),     # For match tests
    ]
    
    # Replace specific instances with unique names
    lines = content.split('\n')
    in_player_test = False
    in_match_test = False
    in_coach_test = False
    
    for i, line in enumerate(lines):
        if 'class TestPlayerModel:' in line:
            in_player_test = True
            in_match_test = False
            in_coach_test = False
        elif 'class TestMatchModel:' in line:
            in_player_test = False
            in_match_test = True
            in_coach_test = False
        elif 'class TestCoachModel:' in line:
            in_player_test = False
            in_match_test = False
            in_coach_test = True
        elif 'class Test' in line:
            in_player_test = False
            in_match_test = False
            in_coach_test = False
        
        if 'Team(name="Test FC"' in line:
            if in_player_test:
                lines[i] = line.replace('Team(name="Test FC"', 'Team(name="Player Test FC"')
            elif in_coach_test:
                lines[i] = line.replace('Team(name="Test FC"', 'Team(name="Coach Test FC"')
        elif 'Team(name="Team A"' in line and in_match_test:
            lines[i] = line.replace('Team(name="Team A"', 'Team(name="Match Team A"')
        elif 'Team(name="Team B"' in line and in_match_test:
            lines[i] = line.replace('Team(name="Team B"', 'Team(name="Match Team B"')
    
    content = '\n'.join(lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed team name conflicts in tests")

if __name__ == "__main__":
    fix_team_name_conflicts()
