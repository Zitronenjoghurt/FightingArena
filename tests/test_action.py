from src.classes.action import ActionFactory
from src.classes.fighter import Fighter

def test_behavior():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    attack1 = ActionFactory.create_action(action_type="attack", action_args={"damage": 10}, user=fighter1)
    attack2 = ActionFactory.create_action(action_type="attack", action_args={"damage": 25}, user=fighter2)

    heal1 = ActionFactory.create_action(action_type="heal", action_args={"mp_cost": 90, "heal_amount": 25}, user=fighter1)
    heal2 = ActionFactory.create_action(action_type="heal", action_args={"mp_cost": 80, "heal_amount": 10}, user=fighter2)

    # attack 1
    assert attack1.is_executable() == True
    attack1.execute(fighter2)
    assert fighter2.get_hp() == 90

    # attack 2
    assert attack2.is_executable() == True
    attack2.execute(fighter1)
    assert fighter1.get_hp() == 75

    # heal 1
    assert heal1.is_executable() == True
    heal1.execute(fighter1)
    assert fighter1.get_hp() == 100
    assert fighter1.get_mp() == 10
    assert heal1.is_executable() == False

    # heal 2
    assert heal2.is_executable() == True
    heal2.execute(fighter2)
    assert fighter2.get_hp() == 100
    assert fighter2.get_mp() == 20
    assert heal2.is_executable() == False