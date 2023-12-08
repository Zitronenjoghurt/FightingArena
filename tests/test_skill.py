from src.classes.fighter import Fighter
from src.classes.skill import Skill

def test_behavior():
    fighter1 = Fighter(max_hp=100, max_mp=10, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    
    fireball = Skill.create_skill(skill_name="debug fireball", fighter=fighter1)
    
    assert fireball.is_usable() == True
    assert fireball.use(fighter2)[0] == True
    fighter1.update()
    fighter2.update()
    assert fireball.is_usable() == False

    assert fighter2.get_hp() == 85
    fighter2.update()
    assert fighter2.get_hp() == 80
    fighter2.update()
    assert fighter2.get_hp() == 75
    fighter2.update()
    assert fighter2.get_hp() == 75

def test_add_user():
    fighter1 = Fighter(max_hp=100, max_mp=10, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    sword_slash = Skill.create_skill(skill_name="debug sword")
    fireball = Skill.create_skill(skill_name="debug fireball")

    fighter1.add_skill(fireball)
    fighter2.add_skill(sword_slash)

    assert fireball.is_usable() == True
    assert fireball.use(fighter2)[0] == True
    fighter1.update()
    fighter2.update()
    assert fireball.is_usable() == False

    assert fighter2.get_hp() == 85
    fighter2.update()
    assert fighter2.get_hp() == 80
    fighter2.update()
    assert fighter2.get_hp() == 75
    fighter2.update()
    assert fighter2.get_hp() == 75

def test_get_categories():
    sword_slash = Skill.create_skill(skill_name="debug sword")
    fireball = Skill.create_skill(skill_name="debug fireball")

    assert sword_slash.get_categories() == ["damage"]
    assert fireball.get_categories() == ["damage", "burning"]

def test_cooldown():
    fighter1 = Fighter(max_hp=100, max_mp=10, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    tackle = Skill("tackle", actions={"attack": {"damage": 10}}, cooldown=3)
    fighter1.add_skill(tackle)

    assert fighter1.use_skill("tackle", fighter2) == True
    assert tackle.get_current_cooldown() == 4
    fighter1.update()
    assert fighter1.use_skill("tackle", fighter2) == False
    assert tackle.get_current_cooldown() == 3
    fighter1.update()
    assert fighter1.use_skill("tackle", fighter2) == False
    assert tackle.get_current_cooldown() == 2
    fighter1.update()
    assert fighter1.use_skill("tackle", fighter2) == False
    assert tackle.get_current_cooldown() == 1
    fighter1.update()
    assert tackle.get_current_cooldown() == 0
    assert fighter1.use_skill("tackle", fighter2) == True
    assert tackle.get_current_cooldown() == 4