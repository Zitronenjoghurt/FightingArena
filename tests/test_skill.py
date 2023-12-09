from src.classes.fighter import Fighter
from src.classes.skill import Skill

def test_sword():
    fighter1 = Fighter(max_hp=100, max_mp=10, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    
    sword = Skill.create_skill(skill_name="debug sword", fighter=fighter1)
    
    assert sword.is_usable() == True
    assert sword.use(fighter2)[0] == True
    fighter1.update()
    fighter2.update()

    assert fighter2.get_hp() == 85

def test_fireball():
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

def test_rest():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter1.set_hp(90)
    fighter1.set_stamina(90)
    fighter2.set_hp(90)
    fighter2.set_stamina(90)
    
    rest = Skill.create_skill(skill_name="debug rest", fighter=fighter1)
    fighter1.add_skill(rest)

    assert rest.is_usable() == True
    assert rest.use(fighter2)[0] == True
    fighter1.update()
    fighter2.update()

    assert rest.is_usable() == False
    assert fighter1.get_hp() == 100
    assert fighter1.get_stamina() == 100
    assert fighter2.get_hp() == 90
    assert fighter2.get_stamina() == 90

    fighter1.update()
    fighter2.update()
    assert rest.is_usable() == False

    fighter1.update()
    fighter2.update()
    assert rest.is_usable() == False

    fighter1.update()
    fighter2.update()
    assert rest.is_usable() == True

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
    assert fireball.get_categories() == ["damage", "burn"]

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