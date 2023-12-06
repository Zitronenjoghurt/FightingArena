from src.classes.fighter import Fighter
from src.classes.skill import Skill

def test_init():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    assert fighter.get_max_hp() == 100
    assert fighter.get_hp() == 100

    assert fighter.get_max_mp() == 100
    assert fighter.get_mp() == 100

    assert fighter.get_max_stamina() == 100
    assert fighter.get_stamina() == 100

def test_load_from_file():
    barbarian = Fighter.load_from_file("barbarian")
    wizard = Fighter.load_from_file("wizard")

    assert barbarian.get_hp() == 100
    assert barbarian.get_mp() == 0
    assert barbarian.get_stamina() == 100
    assert barbarian.skill_usable("sword slash") == True

    assert wizard.get_hp() == 80
    assert wizard.get_mp() == 100
    assert wizard.get_stamina() == 20
    assert wizard.skill_usable("fireball") == True

    assert barbarian.use_skill("sword slash", wizard) == True
    assert barbarian.get_stamina() == 90
    assert wizard.get_hp() == 65

    assert wizard.use_skill("fireball", barbarian) == True
    assert wizard.get_mp() == 90
    assert barbarian.get_hp() == 90

    # fireball burn damage
    barbarian.update()
    assert barbarian.get_hp() == 85
    barbarian.update()
    assert barbarian.get_hp() == 80
    barbarian.update()
    assert barbarian.get_hp() == 75
    barbarian.update()
    assert barbarian.get_hp() == 75

def test_skills():
    fighter1 = Fighter(max_hp=100, max_mp=10, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fireball = Skill.create_skill("fireball", fighter1)
    fighter1.add_skill(fireball)

    assert fighter1.skill_usable("fireball") == True
    assert fighter1.use_skill("fireball", fighter2) == True
    assert fighter1.skill_usable("fireball") == False

    assert fighter2.get_hp() == 90
    fighter2.update()
    assert fighter2.get_hp() == 85
    fighter2.update()
    assert fighter2.get_hp() == 80
    fighter2.update()
    assert fighter2.get_hp() == 75
    fighter2.update()
    assert fighter2.get_hp() == 75

def test_setters():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter.set_max_hp(200)
    fighter.set_max_mp(200)
    fighter.set_max_stamina(200)

    assert fighter.get_max_hp() == 200
    assert fighter.get_max_mp() == 200
    assert fighter.get_max_stamina() == 200

    fighter.set_hp(150)
    fighter.set_mp(150)
    fighter.set_stamina(150)

    assert fighter.get_hp() == 150
    assert fighter.get_mp() == 150
    assert fighter.get_stamina() == 150

def test_remove():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter.remove_hp(50)
    assert fighter.remove_mp(50) == True
    assert fighter.remove_stamina(50) == True

    assert fighter.get_hp() == 50
    assert fighter.get_mp() == 50
    assert fighter.get_stamina() == 50

    fighter.remove_hp(100)
    assert fighter.remove_mp(100) == False
    assert fighter.remove_stamina(100) == False

    assert fighter.get_hp() == 0
    assert fighter.get_mp() == 50
    assert fighter.get_stamina() == 50

def test_add():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter.set_hp(50)
    fighter.set_mp(50)
    fighter.set_stamina(50)

    fighter.add_hp(50)
    fighter.add_mp(50)
    fighter.add_stamina(50)

    assert fighter.get_hp() == 100
    assert fighter.get_mp() == 100
    assert fighter.get_stamina() == 100

    fighter.add_hp(100)
    fighter.add_mp(100)
    fighter.add_stamina(100)

    assert fighter.get_hp() == 100
    assert fighter.get_mp() == 100
    assert fighter.get_stamina() == 100

def test_update():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    
    fighter.remove_hp(50)
    assert fighter.remove_mp(50) == True
    assert fighter.remove_stamina(50) == True

    assert fighter.get_hp() == 50
    assert fighter.get_mp() == 50
    assert fighter.get_stamina() == 50

    fighter.set_max_hp(20)
    fighter.set_max_mp(20)
    fighter.set_max_stamina(20)

    fighter.update()

    assert fighter.get_hp() == 20
    assert fighter.get_mp() == 20
    assert fighter.get_stamina() == 20

def test_get_usable_skills():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    skill1 = Skill(name="stamina_drain", actions={"attack": {"damage": 10, "stamina_cost": 100}})
    skill2 = Skill(name="mp_drain", actions={"attack": {"damage": 10, "mp_cost": 100}})

    fighter1.add_skills([skill1, skill2])
    assert fighter1.get_skills() == [skill1, skill2]

    fighter1.update()

    assert fighter1.get_usable_skills() == [skill1, skill2]
    assert fighter1.get_usable_skill_categories() == ["damage"]
    assert fighter1.get_usable_category_skills() == {"damage": [skill1, skill2]}

    fighter1.use_skill("stamina_drain", fighter2)
    fighter1.update()

    assert fighter1.get_usable_skills() == [skill2]
    assert fighter1.get_usable_skill_categories() == ["damage"]
    assert fighter1.get_usable_category_skills() == {"damage": [skill2]}

    fighter1.use_skill("mp_drain", fighter2)
    fighter1.update()

    assert fighter1.get_usable_skills() == []
    assert fighter1.get_usable_skill_categories() == []
    assert fighter1.get_usable_category_skills() == {}