from src.classes.effect import EffectFactory
from src.classes.fighter import Fighter

def test_behavior():
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