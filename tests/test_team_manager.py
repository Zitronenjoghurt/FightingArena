import pytest
from src.classes.fighter import Fighter
from src.classes.team_manager import TeamManager

@pytest.fixture
def barbarian1():
    return Fighter.load_from_file(".debug_barbarian", "George")

@pytest.fixture
def barbarian2():
    return Fighter.load_from_file(".debug_barbarian", "Karlach")

@pytest.fixture
def wizard1():
    return Fighter.load_from_file(".debug_wizard", "Lisa Lisa")

@pytest.fixture
def wizard2():
    return Fighter.load_from_file(".debug_wizard", "Gandalf")

@pytest.fixture
def team_manager(barbarian1, barbarian2, wizard1, wizard2):
    team_manager = TeamManager()
    team_manager.add_fighters(fighters=[barbarian1, barbarian2], team_name="A")
    team_manager.add_fighters(fighters=[wizard1, wizard2], team_name="B")
    return team_manager

def test_add_fighter(barbarian1, barbarian2, wizard1, wizard2):
    team_manager = TeamManager()

    team_manager.add_fighter(fighter=barbarian1, team_name="A")
    assert team_manager.get_teams() == {"A": [barbarian1]}

    team_manager.add_fighter(fighter=barbarian2, team_name="A")
    assert team_manager.get_teams() == {"A": [barbarian1, barbarian2]}

    team_manager.add_fighters(fighters=[wizard1, wizard2], team_name="B")
    assert team_manager.get_teams() == {"A": [barbarian1, barbarian2], "B": [wizard1, wizard2]}

def test_get_fighters(team_manager: TeamManager, barbarian1: Fighter, barbarian2: Fighter, wizard1: Fighter, wizard2: Fighter):
    wizard1.set_initiative(4)
    barbarian1.set_initiative(3)
    wizard2.set_initiative(2)
    barbarian2.set_initiative(1)

    team_manager.update()

    assert team_manager.get_fighters() == [wizard1, barbarian1, wizard2, barbarian2]

def test_get_fighter_opponents(team_manager: TeamManager, barbarian1: Fighter, barbarian2: Fighter, wizard1: Fighter, wizard2: Fighter):
    assert team_manager.get_fighter_opponents(barbarian1) == [wizard1, wizard2]
    assert team_manager.get_fighter_opponents(barbarian2) == [wizard1, wizard2]
    assert team_manager.get_fighter_opponents(wizard1) == [barbarian1, barbarian2]
    assert team_manager.get_fighter_opponents(wizard2) == [barbarian1, barbarian2]

def test_get_teams(team_manager: TeamManager, barbarian1: Fighter, barbarian2: Fighter, wizard1: Fighter, wizard2: Fighter):
    assert team_manager.get_teams() == {"A": [barbarian1, barbarian2], "B": [wizard1, wizard2]}

def test_get_team_count(team_manager: TeamManager):
    assert team_manager.get_team_count() == 2

def test_get_team_fighters(team_manager: TeamManager, barbarian1: Fighter, barbarian2: Fighter, wizard1: Fighter, wizard2: Fighter):
    assert team_manager.get_team_fighters(team_name="A") == [barbarian1, barbarian2]
    assert team_manager.get_team_fighters(team_name="B") == [wizard1, wizard2]

def test_get_team_opponents(team_manager: TeamManager, barbarian1: Fighter, barbarian2: Fighter, wizard1: Fighter, wizard2: Fighter):
    assert team_manager.get_team_opponents(team_name="A") == [wizard1, wizard2]
    assert team_manager.get_team_opponents(team_name="B") == [barbarian1, barbarian2]

def test_get_roster_string(team_manager: TeamManager):
    assert team_manager.get_roster_string() == "Team A: George, Karlach\nTeam B: Lisa Lisa, Gandalf"