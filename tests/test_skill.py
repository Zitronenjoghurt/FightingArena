from src.classes.fighter import Fighter
from src.classes.skill import Skill

def test_behavior():
    fighter1 = Fighter(max_hp=100, max_mp=10, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    
    fireball = Skill.create_skill(skill_name="fireball", fighter=fighter1)
    
    assert fireball.is_usable() == True
    fireball.use(fighter2)
    assert fireball.is_usable() == False

    assert fighter2.get_hp() == 90
    fighter2.update()
    assert fighter2.get_hp() == 85
    fighter2.update()
    assert fighter2.get_hp() == 80
    fighter2.update()
    assert fighter2.get_hp() == 75
    fighter2.update()
    assert fighter2.get_hp() == 75