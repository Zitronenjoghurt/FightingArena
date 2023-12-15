from src.classes.fighter import Fighter
from src.classes.game_manager import GameManager

def test_init():
    GameManager.reset_instance()

    barbarian = Fighter.load_from_file(".debug_barbarian")
    wizard = Fighter.load_from_file(".debug_wizard")

    gm1 = GameManager.get_instance()
    gm1.add_fighter(fighter=barbarian, team_name="A")
    gm1.add_fighter(fighter=wizard, team_name="B")
    gm2 = GameManager.get_instance()

    assert gm2.team_manager.get_team_names() == ["A", "B"]

def test_example_game():
    GameManager.reset_instance()

    barbarian = Fighter.load_from_file(".debug_barbarian", "Barbarian")
    wizard = Fighter.load_from_file(".debug_wizard", "Wizard")

    gm = GameManager.get_instance(round_time=0)
    gm.add_fighter(fighter=barbarian, team_name="A")
    gm.add_fighter(fighter=wizard, team_name="B")
    gm.start_game()

    # ROUND 0
    assert gm.log.get_round_log(0)[gm.LOG_GAME_STATUS_TOP] == ['==================={FIGHT START}==================', 'Team A: Barbarian\nTeam B: Wizard', '==================================================']

    # ROUND 1
    assert gm.log.get_round_log(1)[gm.LOG_GAME_STATUS_TOP]             == ['[ROUND 1]']
    assert gm.log.get_round_log(1)[gm.LOG_SKILL_USE]                   == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(1)[gm.LOG_EFFECT_APPLY]                == ['Barbarian received effect: burning']
    assert gm.log.get_round_log(1)[gm.LOG_EFFECT_EXECUTE]              == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(1)[gm.LOG_DEBUG_FIGHTER_STATUS_RAW][0] == [['[Barbarian]', '85 (-15)', '0 (0)', '90 (-10)'], ['[Wizard]', '65 (-15)', '90 (-10)', '20 (0)']]

    # ROUND 2
    assert gm.log.get_round_log(2)[gm.LOG_GAME_STATUS_TOP]              == ['[ROUND 2]']
    assert gm.log.get_round_log(2)[gm.LOG_SKILL_USE]                    == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(2)[gm.LOG_EFFECT_APPLY]                 == ['Barbarian already has effect: burning']
    assert gm.log.get_round_log(2)[gm.LOG_EFFECT_EXECUTE]               == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(2)[gm.LOG_DEBUG_FIGHTER_STATUS_RAW][0]  == [['[Barbarian]', '70 (-15)', '0 (0)', '80 (-10)'], ['[Wizard]', '50 (-15)', '80 (-10)', '20 (0)']]

    # ROUND 3
    assert gm.log.get_round_log(3)[gm.LOG_GAME_STATUS_TOP]              == ['[ROUND 3]']
    assert gm.log.get_round_log(3)[gm.LOG_SKILL_USE]                    == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(3)[gm.LOG_EFFECT_APPLY]                 == ['Barbarian already has effect: burning']
    assert gm.log.get_round_log(3)[gm.LOG_EFFECT_EXECUTE]               == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(3)[gm.LOG_EFFECT_REMOVE]                == ['Barbarian lost effect: burning']
    assert gm.log.get_round_log(3)[gm.LOG_DEBUG_FIGHTER_STATUS_RAW][0]  == [['[Barbarian]', '55 (-15)', '0 (0)', '70 (-10)'], ['[Wizard]', '35 (-15)', '70 (-10)', '20 (0)']]

    # ROUND 4
    assert gm.log.get_round_log(4)[gm.LOG_GAME_STATUS_TOP]              == ['[ROUND 4]']
    assert gm.log.get_round_log(4)[gm.LOG_SKILL_USE]                    == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(4)[gm.LOG_EFFECT_APPLY]                 == ['Barbarian received effect: burning']
    assert gm.log.get_round_log(4)[gm.LOG_EFFECT_EXECUTE]               == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(4)[gm.LOG_DEBUG_FIGHTER_STATUS_RAW][0]  == [['[Barbarian]', '40 (-15)', '0 (0)', '60 (-10)'], ['[Wizard]', '20 (-15)', '60 (-10)', '20 (0)']]

    # ROUND 5
    assert gm.log.get_round_log(5)[gm.LOG_GAME_STATUS_TOP]              == ['[ROUND 5]']
    assert gm.log.get_round_log(5)[gm.LOG_SKILL_USE]                    == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(5)[gm.LOG_EFFECT_APPLY]                 == ['Barbarian already has effect: burning']
    assert gm.log.get_round_log(5)[gm.LOG_EFFECT_EXECUTE]               == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(5)[gm.LOG_DEBUG_FIGHTER_STATUS_RAW][0]  == [['[Barbarian]', '25 (-15)', '0 (0)', '50 (-10)'], ['[Wizard]', '5 (-15)', '50 (-10)', '20 (0)']]

    # ROUND 6
    assert gm.log.get_round_log(6)[gm.LOG_GAME_STATUS_TOP]             == ['[ROUND 6]']
    assert gm.log.get_round_log(6)[gm.LOG_SKILL_USE]                   == ['Barbarian uses their sword to slash Wizard.', 'Wizard throws fireball at Barbarian.']
    assert gm.log.get_round_log(6)[gm.LOG_EFFECT_APPLY]                == ['Barbarian already has effect: burning']
    assert gm.log.get_round_log(6)[gm.LOG_EFFECT_EXECUTE]              == ['Barbarian is burning, -5HP']
    assert gm.log.get_round_log(6)[gm.LOG_EFFECT_REMOVE]               == ['Barbarian lost effect: burning']
    assert gm.log.get_round_log(6)[gm.LOG_DEBUG_FIGHTER_STATUS_RAW][0] == [['[Barbarian]', '10 (-15)', '0 (0)', '40 (-10)'], ['[Wizard]', '0 (-5)', '40 (-10)', '20 (0)']]
    assert gm.log.get_round_log(6)[gm.LOG_GAME_FINISH]                 == ['TEAM A WINS!!!']

def test_check_win_condition():
    GameManager.reset_instance()

    barbarian1 = Fighter.load_from_file(".debug_barbarian")
    barbarian2 = Fighter.load_from_file(".debug_barbarian")
    wizard1 = Fighter.load_from_file(".debug_wizard")
    wizard2 = Fighter.load_from_file(".debug_wizard")

    gm = GameManager.get_instance()
    gm.add_fighters(fighters=[barbarian1, barbarian2], team_name="A")
    gm.add_fighters(fighters=[wizard1, wizard2], team_name="B")

    assert gm.check_win_condition() == set()

    barbarian1.set_hp(0)
    assert gm.check_win_condition() == set()

    barbarian2.set_hp(0)
    assert gm.check_win_condition() == set("B")

def test_is_tie():
    GameManager.reset_instance()

    barbarian = Fighter.load_from_file(".debug_barbarian")
    wizard = Fighter.load_from_file(".debug_wizard")

    barbarian.set_hp(0)
    wizard.set_hp(0)

    gm = GameManager.get_instance(print_log=False, round_time=0, max_rounds=100)
    gm.add_fighter(fighter=barbarian, team_name="A")
    gm.add_fighter(fighter=wizard, team_name="B")
    gm.start_game()

    assert gm.is_tie() == True