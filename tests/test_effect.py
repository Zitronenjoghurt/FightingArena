from src.classes.effect import EffectFactory
from src.classes.fighter import Fighter
from src.classes.skill import Skill

def test_burn():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    burn = EffectFactory.create_effect("burn", {"duration": 3, "damage": 10})
    fighter.apply_effect(burn)

    fighter.update()
    assert fighter.get_hp() == 90
    fighter.update()
    assert fighter.get_hp() == 80
    fighter.update()
    assert fighter.get_hp() == 70
    fighter.update()
    assert fighter.get_hp() == 70

def test_freeze():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    skill = Skill(name="sword slash", actions={"attack": {"damage": 10, "stamina_cost": 10}})
    freeze = EffectFactory.create_effect("freeze", {"duration": 3})

    fighter1.add_skill(skill=skill)
    fighter1.apply_effect(freeze)

    assert fighter1.use_skill("sword slash", fighter2) == False
    fighter1.update()
    assert fighter1.use_skill("sword slash", fighter2) == False
    fighter1.update()
    assert fighter1.use_skill("sword slash", fighter2) == False
    fighter1.update()
    assert fighter1.use_skill("sword slash", fighter2) == True