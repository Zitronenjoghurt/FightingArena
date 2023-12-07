from src.classes.action import ActionFactory
from src.classes.fighter import Fighter

def test_attack():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    attack1 = ActionFactory.create_action(action_type="attack", action_args={"damage": 10}, user=fighter1)
    attack2 = ActionFactory.create_action(action_type="attack", action_args={"damage": 25}, user=fighter2)

    assert attack1.is_executable() == True
    assert attack1.execute(fighter2) == True
    fighter2.update()
    assert fighter2.get_hp() == 90

    assert attack2.is_executable() == True
    assert attack2.execute(fighter1) == True
    fighter1.update()
    assert fighter1.get_hp() == 75
    

def test_heal():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter1.set_hp(75)
    fighter2.set_hp(90)

    heal1 = ActionFactory.create_action(action_type="heal", action_args={"mp_cost": 90, "amount": 25}, user=fighter1)
    heal2 = ActionFactory.create_action(action_type="heal", action_args={"mp_cost": 80, "amount": 10}, user=fighter2)

    # heal 1
    assert heal1.is_executable() == True
    assert heal1.execute(fighter1) == True
    fighter1.update()
    fighter2.update()
    assert fighter1.get_hp() == 100
    assert fighter1.get_mp() == 10
    assert heal1.is_executable() == False

    # heal 2
    assert heal2.is_executable() == True
    assert heal2.execute(fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter2.get_hp() == 100
    assert fighter2.get_mp() == 20
    assert heal2.is_executable() == False

def test_lifesteal():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter1.set_hp(50)
    fighter2.set_hp(50)

    lifesteal1 = ActionFactory.create_action(action_type="lifesteal", action_args={"damage": 10, "heal": 20, "mp_cost": 60}, user=fighter1)
    lifesteal2 = ActionFactory.create_action(action_type="lifesteal", action_args={"damage": 10, "damage_is_heal": True, "heal_multiplier": 2, "mp_cost": 60}, user=fighter2)

    # lifesteal 1
    assert lifesteal1.is_executable() == True
    assert lifesteal1.execute(fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter1.get_hp() == 70
    assert fighter1.get_mp() == 40
    assert fighter2.get_hp() == 40
    assert lifesteal1.is_executable() == False

    # lifesteal 2
    assert lifesteal2.is_executable() == True
    assert lifesteal2.execute(fighter1) == True
    fighter1.update()
    fighter2.update()
    assert fighter1.get_hp() == 60
    assert fighter2.get_hp() == 60
    assert fighter2.get_mp() == 40
    assert lifesteal2.is_executable() == False