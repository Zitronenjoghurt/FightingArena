from src.classes.effect import EffectFactory
from src.classes.fighter import Fighter
from src.classes.game_manager import GameManager
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
    barbarian = Fighter.load_from_file(".debug_barbarian", "George")
    wizard = Fighter.load_from_file(".debug_wizard", "Gandalf")

    assert barbarian.get_name() == "George"
    assert barbarian.get_hp() == 100
    assert barbarian.get_mp() == 0
    assert barbarian.get_stamina() == 100
    assert barbarian.skill_usable("debug sword") == True

    assert wizard.get_name() == "Gandalf"
    assert wizard.get_hp() == 80
    assert wizard.get_mp() == 100
    assert wizard.get_stamina() == 20
    assert wizard.skill_usable("debug fireball") == True

    assert barbarian.use_skill("debug sword", wizard) == True
    barbarian.update()
    wizard.update()
    assert barbarian.get_stamina() == 90
    assert wizard.get_hp() == 65

    assert wizard.use_skill("debug fireball", barbarian) == True
    barbarian.update()
    wizard.update()
    assert wizard.get_mp() == 90
    assert barbarian.get_hp() == 85

    # fireball burn damage
    barbarian.update()
    assert barbarian.get_hp() == 80
    barbarian.update()
    assert barbarian.get_hp() == 75
    barbarian.update()
    assert barbarian.get_hp() == 75

def test_skills():
    fighter1 = Fighter(max_hp=100, max_mp=10, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fireball = Skill.create_skill("debug fireball", fighter1)
    fighter1.add_skill(fireball)

    assert fighter1.skill_usable("debug fireball") == True
    assert fighter1.use_skill("debug fireball", fighter2) == True
    fighter1.update()
    fighter2.update()
    assert fighter1.skill_usable("debug fireball") == False

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

    assert fighter.get_name() == "no_name"
    assert fighter.get_team() == ""
    assert fighter.get_max_hp() == 200
    assert fighter.get_max_mp() == 200
    assert fighter.get_max_stamina() == 200

    fighter.set_name("George")
    fighter.set_team("A")
    fighter.set_hp(150)
    fighter.set_mp(150)
    fighter.set_stamina(150)

    assert fighter.get_name() == "George"
    assert fighter.get_team() == "A"
    assert fighter.get_hp() == 150
    assert fighter.get_mp() == 150
    assert fighter.get_stamina() == 150

def test_remove():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter.remove_hp(50)
    assert fighter.remove_mp(50) == True
    assert fighter.remove_stamina(50) == True

    assert fighter.hp_difference == -50
    assert fighter.mp_difference == -50
    assert fighter.stamina_difference == -50

    fighter.update()

    assert fighter.get_hp() == 50
    assert fighter.get_mp() == 50
    assert fighter.get_stamina() == 50
    assert fighter.hp_difference == 0
    assert fighter.mp_difference == 0
    assert fighter.stamina_difference == 0
    assert fighter.previous_hp_difference == -50
    assert fighter.previous_mp_difference == -50
    assert fighter.previous_stamina_difference == -50

    fighter.remove_hp(100)
    assert fighter.remove_mp(100) == False
    assert fighter.remove_stamina(100) == False
    assert fighter.hp_difference == -50
    assert fighter.mp_difference == 0
    assert fighter.stamina_difference == 0

    fighter.update()

    assert fighter.get_hp() == 0
    assert fighter.get_mp() == 50
    assert fighter.get_stamina() == 50
    assert fighter.hp_difference == 0
    assert fighter.mp_difference == 0
    assert fighter.stamina_difference == 0
    assert fighter.previous_hp_difference == -50
    assert fighter.previous_mp_difference == 0
    assert fighter.previous_stamina_difference == 0

def test_add():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    fighter.set_hp(50)
    fighter.set_mp(50)
    fighter.set_stamina(50)

    fighter.add_hp(50)
    fighter.add_mp(50)
    fighter.add_stamina(50)

    assert fighter.hp_difference == 50
    assert fighter.mp_difference == 50
    assert fighter.stamina_difference == 50

    fighter.update()

    assert fighter.get_hp() == 100
    assert fighter.get_mp() == 100
    assert fighter.get_stamina() == 100
    assert fighter.hp_difference == 0
    assert fighter.mp_difference == 0
    assert fighter.stamina_difference == 0
    assert fighter.previous_hp_difference == 50
    assert fighter.previous_mp_difference == 50
    assert fighter.previous_stamina_difference == 50

    fighter.set_hp(80)

    fighter.add_hp(100)
    fighter.add_mp(100)
    fighter.add_stamina(100)

    assert fighter.hp_difference == 20
    assert fighter.mp_difference == 0
    assert fighter.stamina_difference == 0

    fighter.update()

    assert fighter.get_hp() == 100
    assert fighter.get_mp() == 100
    assert fighter.get_stamina() == 100
    assert fighter.hp_difference == 0
    assert fighter.mp_difference == 0
    assert fighter.stamina_difference == 0
    assert fighter.previous_hp_difference == 20
    assert fighter.previous_mp_difference == 0
    assert fighter.previous_stamina_difference == 0

def test_update():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    
    fighter.remove_hp(50)
    assert fighter.remove_mp(50) == True
    assert fighter.remove_stamina(50) == True

    fighter.update()

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

    skill1 = Skill(name="stamina_drain", actions={"attack": {"damage": 10}}, stamina_cost=100)
    skill2 = Skill(name="mp_drain", actions={"attack": {"damage": 10}}, mp_cost=100)

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

def test_apply_effects():
    GameManager.reset_instance()
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    burn = EffectFactory.create_effect("burn", {"duration": 3, "damage": 10})
    teams = {"A": [fighter1]}

    gm = GameManager.get_instance(teams=teams)

    fighter1.apply_effect(burn)
    assert gm.log.get_round_log(0) == {"effect_apply": ['no_name received effect: burning']}

    fighter1.apply_effect(burn)
    assert gm.log.get_round_log(0) == {"effect_apply": ['no_name received effect: burning', 'no_name already has effect: burning']}

def test_get_effects():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    burn = EffectFactory.create_effect("burn", {"duration": 3, "damage": 10})
    freeze = EffectFactory.create_effect("freeze", {"duration": 3})

    fighter.apply_effect(burn)
    fighter.apply_effect(freeze)

    assert fighter.get_effects() == ["burning", "frozen"]

def test_has_effect():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    burn = EffectFactory.create_effect("burn", {"duration": 3, "damage": 10})
    freeze = EffectFactory.create_effect("freeze", {"duration": 3})

    fighter.apply_effect(burn)
    fighter.apply_effect(freeze)

    assert fighter.has_effect("frozen") == True
    assert fighter.has_effect("burning") == True
    assert fighter.has_effect("donkey doodoo") == False

    assert fighter.has_effects(["frozen", "donkey doodoo"]) == True
    assert fighter.has_effects(["donkey doodoo"]) == False

def test_can_attack():
    fighter1 = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    fighter2 = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    skill = Skill(name="stamina_drain", actions={"attack": {"damage": 10}}, stamina_cost=10)
    fighter1.add_skill(skill=skill)

    assert fighter1.can_attack() == True
    fighter1.disallow_attack()
    assert fighter1.can_attack() == False

    assert fighter1.use_skill("stamina_drain", fighter2) == False
    assert fighter1.has_attacked() == False

    fighter1.allow_attack()
    assert fighter1.can_attack() == True
    assert fighter1.use_skill("stamina_drain", fighter2) == True
    assert fighter1.has_attacked() == True