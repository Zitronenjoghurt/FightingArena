from src.classes.action import ActionFactory
from src.classes.fighter import Fighter

def test_attack():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    attack1 = ActionFactory.create_action(action_type="attack", action_args={"damage": 10, "on_target": True}, user=fighter1)
    attack2 = ActionFactory.create_action(action_type="attack", action_args={"damage": 25, "on_target": True}, user=fighter2)

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

    heal1 = ActionFactory.create_action(action_type="heal", action_args={"amount": 25, "on_self": True}, user=fighter1)
    heal2 = ActionFactory.create_action(action_type="heal", action_args={"amount": 10, "on_target": True}, user=fighter2)

    # heal 1
    assert heal1.is_executable() == True
    assert heal1.execute(fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter1.get_hp() == 100

    # heal 2
    assert heal2.is_executable() == True
    assert heal2.execute(fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter2.get_hp() == 100

def test_regen_mp():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter1.set_mp(75)
    fighter2.set_mp(90)

    regen1 = ActionFactory.create_action(action_type="regen_mp", action_args={"amount": 25, "on_self": True}, user=fighter1)
    regen2 = ActionFactory.create_action(action_type="regen_mp", action_args={"amount": 10, "on_target": True}, user=fighter2)

    # regen 1
    assert regen1.is_executable() == True
    assert regen1.execute(fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter1.get_mp() == 100

    # regen 2
    assert regen2.is_executable() == True
    assert regen2.execute(fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter2.get_mp() == 100

def test_regen_stamina():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter1.set_stamina(75)
    fighter2.set_stamina(90)

    regen1 = ActionFactory.create_action(action_type="regen_stamina", action_args={"amount": 25, "on_self": True}, user=fighter1)
    regen2 = ActionFactory.create_action(action_type="regen_stamina", action_args={"amount": 10, "on_target": True}, user=fighter2)

    # regen 1
    assert regen1.is_executable() == True
    assert regen1.execute(fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter1.get_stamina() == 100

    # regen 2
    assert regen2.is_executable() == True
    assert regen2.execute(fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter2.get_stamina() == 100

def test_lifesteal():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter1.set_hp(50)
    fighter2.set_hp(50)

    lifesteal1 = ActionFactory.create_action(action_type="lifesteal", action_args={"damage": 10, "heal": 20}, user=fighter1)
    lifesteal2 = ActionFactory.create_action(action_type="lifesteal", action_args={"damage": 10, "damage_is_heal": True, "heal_multiplier": 2}, user=fighter2)

    # lifesteal 1
    assert lifesteal1.is_executable() == True
    assert lifesteal1.execute(fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter1.get_hp() == 70
    assert fighter2.get_hp() == 40

    # lifesteal 2
    assert lifesteal2.is_executable() == True
    assert lifesteal2.execute(fighter1) == True
    fighter1.update()
    fighter2.update()
    assert fighter1.get_hp() == 60
    assert fighter2.get_hp() == 60