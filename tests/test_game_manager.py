from src.classes.fighter import Fighter
from src.classes.game_manager import GameManager

def test_init():
    GameManager.reset_instance()

    barbarian = Fighter.load_from_file("debug_barbarian")
    wizard = Fighter.load_from_file("debug_wizard")

    teams = {"A": [barbarian], "B": [wizard]}

    gm1 = GameManager.get_instance(teams=teams)
    gm2 = GameManager.get_instance()

    assert gm2.get_team_names() == ["A", "B"]

def test_example_game():
    ROUND1 = {'skill_use': ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.'], 'effect_apply': ['Barbarian received effect: burn'], 'effect_execute': ['Barbarian is burning, -5HP'], 'fighter_status': ['[Barbarian] 85HP | 0MP | 90ST', '[Wizard] 65HP | 90MP | 20ST']}
    ROUND2 = {'skill_use': ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.'], 'effect_apply': ['Barbarian already has effect: burn'], 'effect_execute': ['Barbarian is burning, -5HP'], 'fighter_status': ['[Barbarian] 70HP | 0MP | 80ST', '[Wizard] 50HP | 80MP | 20ST']}
    ROUND3 = {'skill_use': ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.'], 'effect_apply': ['Barbarian already has effect: burn'], 'effect_execute': ['Barbarian is burning, -5HP'], 'effect_remove': ['Barbarian lost effect: burn'], 'fighter_status': ['[Barbarian] 55HP | 0MP | 70ST', '[Wizard] 35HP | 70MP | 20ST']}
    ROUND4 = {'skill_use': ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.'], 'effect_apply': ['Barbarian received effect: burn'], 'effect_execute': ['Barbarian is burning, -5HP'], 'fighter_status': ['[Barbarian] 40HP | 0MP | 60ST', '[Wizard] 20HP | 60MP | 20ST']}
    ROUND5 = {'skill_use': ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.'], 'effect_apply': ['Barbarian already has effect: burn'], 'effect_execute': ['Barbarian is burning, -5HP'], 'fighter_status': ['[Barbarian] 25HP | 0MP | 50ST', '[Wizard] 5HP | 50MP | 20ST']}
    ROUND6 = {'skill_use': ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.'], 'effect_apply': ['Barbarian already has effect: burn'], 'effect_execute': ['Barbarian is burning, -5HP'], 'effect_remove': ['Barbarian lost effect: burn'], 'fighter_status': ['[Barbarian] 10HP | 0MP | 40ST', '[Wizard] 0HP | 40MP | 20ST'], 'game_finish': ['\nTEAM A WINS!!!']}

    GameManager.reset_instance()

    barbarian = Fighter.load_from_file("debug_barbarian", "Barbarian")
    wizard = Fighter.load_from_file("debug_wizard", "Wizard")

    teams = {"A": [barbarian], "B": [wizard]}

    gm = GameManager.get_instance(teams=teams, round_time=0)
    gm.start_game()

    assert gm.log.get_round_log(1) == ROUND1
    assert gm.log.get_round_log(2) == ROUND2
    assert gm.log.get_round_log(3) == ROUND3
    assert gm.log.get_round_log(4) == ROUND4
    assert gm.log.get_round_log(5) == ROUND5
    assert gm.log.get_round_log(6) == ROUND6

def test_add_teams():
    GameManager.reset_instance()

    barbarian1 = Fighter.load_from_file("debug_barbarian")
    barbarian2 = Fighter.load_from_file("debug_barbarian")
    wizard1 = Fighter.load_from_file("debug_wizard")
    wizard2 = Fighter.load_from_file("debug_wizard")

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
    GameManager.reset_instance()

    barbarian1 = Fighter.load_from_file("debug_barbarian")
    barbarian2 = Fighter.load_from_file("debug_barbarian")
    wizard1 = Fighter.load_from_file("debug_wizard")
    wizard2 = Fighter.load_from_file("debug_wizard")

    teams = {"A": [barbarian1, barbarian2], "B": [wizard1, wizard2]}
    gm = GameManager.get_instance(teams=teams)

    assert gm.get_team_name(barbarian1) == "A"
    assert gm.get_team_name(barbarian2) == "A"
    assert gm.get_team_name(wizard1) == "B"
    assert gm.get_team_name(wizard2) == "B"
    assert gm.get_team_names() == ["A", "B"]

    gm.reset_instance()

def test_get_fighter_team():
    GameManager.reset_instance()

    barbarian1 = Fighter.load_from_file("debug_barbarian")
    barbarian2 = Fighter.load_from_file("debug_barbarian")
    wizard1 = Fighter.load_from_file("debug_wizard")
    wizard2 = Fighter.load_from_file("debug_wizard")

    teams = {"A": [barbarian1, barbarian2], "B": [wizard1, wizard2]}
    gm = GameManager.get_instance(teams=teams)

    assert barbarian1.get_team() == "A"
    assert barbarian2.get_team() == "A"
    assert wizard1.get_team() == "B"
    assert wizard2.get_team() == "B"
    
    gm.reset_instance()

def test_get_opponents():
    GameManager.reset_instance()
    
    barbarian1 = Fighter.load_from_file("debug_barbarian")
    barbarian2 = Fighter.load_from_file("debug_barbarian")
    wizard1 = Fighter.load_from_file("debug_wizard")
    wizard2 = Fighter.load_from_file("debug_wizard")

    teams = {"A": [barbarian1, barbarian2], "B": [wizard1, wizard2]}
    gm = GameManager.get_instance(teams=teams)

    assert gm.get_opponents(barbarian1) == [wizard1, wizard2]
    assert gm.get_opponents(barbarian2) == [wizard1, wizard2]
    assert gm.get_opponents(wizard1) == [barbarian1, barbarian2]
    assert gm.get_opponents(wizard2) == [barbarian1, barbarian2]

    gm.reset_instance()

def test_check_win_condition():
    GameManager.reset_instance()

    barbarian1 = Fighter.load_from_file("debug_barbarian")
    barbarian2 = Fighter.load_from_file("debug_barbarian")
    wizard1 = Fighter.load_from_file("debug_wizard")
    wizard2 = Fighter.load_from_file("debug_wizard")

    teams = {"A": [barbarian1, barbarian2], "B": [wizard1, wizard2]}
    gm = GameManager.get_instance(teams=teams)

    assert gm.check_win_condition() == set()

    barbarian1.set_hp(0)
    assert gm.check_win_condition() == set()

    barbarian2.set_hp(0)
    assert gm.check_win_condition() == set("B")