from src.classes.fighter import Fighter
from src.classes.game_manager import GameManager

def test_init():
    barbarian = Fighter.load_from_file("barbarian")
    wizard = Fighter.load_from_file("wizard")

    teams = {"A": [barbarian], "B": [wizard]}

    gm1 = GameManager.get_instance(teams=teams)
    gm2 = GameManager.get_instance()

    assert gm2.get_team_names() == ["A", "B"]

    gm1.reset_instance()

def test_add_teams():
    barbarian1 = Fighter.load_from_file("barbarian")
    barbarian2 = Fighter.load_from_file("barbarian")
    wizard1 = Fighter.load_from_file("wizard")
    wizard2 = Fighter.load_from_file("wizard")

    teams = {"A": [barbarian1]}
    gm = GameManager.get_instance(teams=teams)
    teams = {"A": [barbarian2], "B": [wizard1, wizard2]}
    gm.add_teams(teams=teams)

    assert gm.get_team_names() == ["A", "B"]
    assert gm.get_fighters() == [barbarian1, barbarian2, wizard1, wizard2]
    assert gm.get_team_fighters("A") == [barbarian1, barbarian2]
    assert gm.get_team_fighters("B") == [wizard1, wizard2]

    gm.reset_instance()

def test_get_team_name():
    barbarian1 = Fighter.load_from_file("barbarian")
    barbarian2 = Fighter.load_from_file("barbarian")
    wizard1 = Fighter.load_from_file("wizard")
    wizard2 = Fighter.load_from_file("wizard")

    teams = {"A": [barbarian1, barbarian2], "B": [wizard1, wizard2]}
    gm = GameManager.get_instance(teams=teams)

    assert gm.get_team_name(barbarian1) == "A"
    assert gm.get_team_name(barbarian2) == "A"
    assert gm.get_team_name(wizard1) == "B"
    assert gm.get_team_name(wizard2) == "B"
    assert gm.get_team_names() == ["A", "B"]

    gm.reset_instance()

def test_get_fighter_team():
    barbarian1 = Fighter.load_from_file("barbarian")
    barbarian2 = Fighter.load_from_file("barbarian")
    wizard1 = Fighter.load_from_file("wizard")
    wizard2 = Fighter.load_from_file("wizard")

    teams = {"A": [barbarian1, barbarian2], "B": [wizard1, wizard2]}
    gm = GameManager.get_instance(teams=teams)

    assert gm.get_fighter_team(barbarian1) == "A"
    assert gm.get_fighter_team(barbarian2) == "A"
    assert gm.get_fighter_team(wizard1) == "B"
    assert gm.get_fighter_team(wizard2) == "B"
    
    gm.reset_instance()

def test_get_opponents():
    barbarian1 = Fighter.load_from_file("barbarian")
    barbarian2 = Fighter.load_from_file("barbarian")
    wizard1 = Fighter.load_from_file("wizard")
    wizard2 = Fighter.load_from_file("wizard")

    teams = {"A": [barbarian1, barbarian2], "B": [wizard1, wizard2]}
    gm = GameManager.get_instance(teams=teams)

    assert gm.get_opponents(barbarian1) == [wizard1, wizard2]
    assert gm.get_opponents(barbarian2) == [wizard1, wizard2]
    assert gm.get_opponents(wizard1) == [barbarian1, barbarian2]
    assert gm.get_opponents(wizard2) == [barbarian1, barbarian2]

    gm.reset_instance()