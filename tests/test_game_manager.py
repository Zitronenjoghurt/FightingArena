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
    GameManager.reset_instance()

    barbarian = Fighter.load_from_file("debug_barbarian", "Barbarian")
    wizard = Fighter.load_from_file("debug_wizard", "Wizard")

    teams = {"A": [barbarian], "B": [wizard]}

    gm = GameManager.get_instance(teams=teams, round_time=0)
    gm.start_game()

    # ROUND 0
    assert gm.log.get_round_log(0)[gm.LOG_GAME_STATUS_TOP] == ['==================={FIGHT START}==================', 'Team A: Barbarian', 'Team B: Wizard', '==================================================']

    # ROUND 1
    assert gm.log.get_round_log(1)[gm.LOG_GAME_STATUS_TOP] == ['[ROUND 1]']
    assert gm.log.get_round_log(1)[gm.LOG_SKILL_USE]       == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(1)[gm.LOG_EFFECT_APPLY]    == ['Barbarian received effect: burn']
    assert gm.log.get_round_log(1)[gm.LOG_EFFECT_EXECUTE]  == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(1)[gm.LOG_FIGHTER_STATUS]  == ['[Barbarian] 85HP(-15) | 0MP(0) | 90ST(-10)', '[Wizard] 65HP(-15) | 90MP(-10) | 20ST(0)']

    # ROUND 2
    assert gm.log.get_round_log(2)[gm.LOG_GAME_STATUS_TOP] == ['[ROUND 2]']
    assert gm.log.get_round_log(2)[gm.LOG_SKILL_USE]       == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(2)[gm.LOG_EFFECT_APPLY]    == ['Barbarian already has effect: burn']
    assert gm.log.get_round_log(2)[gm.LOG_EFFECT_EXECUTE]  == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(2)[gm.LOG_FIGHTER_STATUS]  == ['[Barbarian] 70HP(-15) | 0MP(0) | 80ST(-10)', '[Wizard] 50HP(-15) | 80MP(-10) | 20ST(0)']

    # ROUND 3
    assert gm.log.get_round_log(3)[gm.LOG_GAME_STATUS_TOP] == ['[ROUND 3]']
    assert gm.log.get_round_log(3)[gm.LOG_SKILL_USE]       == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(3)[gm.LOG_EFFECT_APPLY]    == ['Barbarian already has effect: burn']
    assert gm.log.get_round_log(3)[gm.LOG_EFFECT_EXECUTE]  == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(3)[gm.LOG_EFFECT_REMOVE]   == ['Barbarian lost effect: burn']
    assert gm.log.get_round_log(3)[gm.LOG_FIGHTER_STATUS]  == ['[Barbarian] 55HP(-15) | 0MP(0) | 70ST(-10)', '[Wizard] 35HP(-15) | 70MP(-10) | 20ST(0)']

    # ROUND 4
    assert gm.log.get_round_log(4)[gm.LOG_GAME_STATUS_TOP] == ['[ROUND 4]']
    assert gm.log.get_round_log(4)[gm.LOG_SKILL_USE]       == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(4)[gm.LOG_EFFECT_APPLY]    == ['Barbarian received effect: burn']
    assert gm.log.get_round_log(4)[gm.LOG_EFFECT_EXECUTE]  == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(4)[gm.LOG_FIGHTER_STATUS]  == ['[Barbarian] 40HP(-15) | 0MP(0) | 60ST(-10)', '[Wizard] 20HP(-15) | 60MP(-10) | 20ST(0)']

    # ROUND 5
    assert gm.log.get_round_log(5)[gm.LOG_GAME_STATUS_TOP] == ['[ROUND 5]']
    assert gm.log.get_round_log(5)[gm.LOG_SKILL_USE]       == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(5)[gm.LOG_EFFECT_APPLY]    == ['Barbarian already has effect: burn']
    assert gm.log.get_round_log(5)[gm.LOG_EFFECT_EXECUTE]  == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(5)[gm.LOG_FIGHTER_STATUS]  == ['[Barbarian] 25HP(-15) | 0MP(0) | 50ST(-10)', '[Wizard] 5HP(-15) | 50MP(-10) | 20ST(0)']

    # ROUND 6
    assert gm.log.get_round_log(6)[gm.LOG_GAME_STATUS_TOP] == ['[ROUND 6]']
    assert gm.log.get_round_log(6)[gm.LOG_SKILL_USE]       == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(6)[gm.LOG_EFFECT_APPLY]    == ['Barbarian already has effect: burn']
    assert gm.log.get_round_log(6)[gm.LOG_EFFECT_EXECUTE]  == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(6)[gm.LOG_EFFECT_REMOVE]   == ['Barbarian lost effect: burn']
    assert gm.log.get_round_log(6)[gm.LOG_FIGHTER_STATUS]  == ['[Barbarian] 10HP(-15) | 0MP(0) | 40ST(-10)', '[Wizard] 0HP(-5) | 40MP(-10) | 20ST(0)']
    assert gm.log.get_round_log(6)[gm.LOG_GAME_FINISH]     == ['TEAM A WINS!!!']

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