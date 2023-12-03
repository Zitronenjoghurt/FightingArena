from src.classes.fighter import Fighter

def test_init():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)

    assert fighter.get_max_hp() == 100
    assert fighter.get_hp() == 100
    assert fighter.get_hp_regen() == 0

    assert fighter.get_max_mp() == 100
    assert fighter.get_mp() == 100
    assert fighter.get_mp_regen() == 0

    assert fighter.get_max_stamina() == 100
    assert fighter.get_stamina() == 100
    assert fighter.get_stamina_regen() == 0

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

    fighter.set_hp_regen(2)
    fighter.set_mp_regen(2)
    fighter.set_stamina_regen(2)

    assert fighter.get_hp_regen() == 2
    assert fighter.get_mp_regen() == 2
    assert fighter.get_stamina_regen() == 2

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

def test_update():
    fighter = Fighter(max_hp=100, max_mp=100, max_stamina=100)
    
    fighter.remove_hp(50)
    assert fighter.remove_mp(50) == True
    assert fighter.remove_stamina(50) == True

    assert fighter.get_hp() == 50
    assert fighter.get_mp() == 50
    assert fighter.get_stamina() == 50

    fighter.set_hp_regen(1)
    fighter.set_mp_regen(1)
    fighter.set_stamina_regen(1)

    fighter.update()

    assert fighter.get_hp() == 51
    assert fighter.get_mp() == 51
    assert fighter.get_stamina() == 51