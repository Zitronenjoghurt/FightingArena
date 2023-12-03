class Fighter():
    def __init__(self,
                 max_hp: int = 0,
                 max_mp: int = 0,
                 max_stamina: int = 0
                 ) -> None:
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.hp_regen = 0

        self.max_mp = max_mp
        self.mp = self.max_mp
        self.mp_regen = 0

        self.max_stamina = max_stamina
        self.stamina = self.max_stamina
        self.stamina_regen = 0

    def update(self) -> None:
        self.hp += self.hp_regen
        self.mp += self.mp_regen
        self.stamina += self.stamina_regen

        self.hp = min(self.hp, self.max_hp)
        self.mp = min(self.mp, self.max_mp)
        self.stamina = min(self.stamina, self.max_stamina)

    def get_max_hp(self) -> int:
        return self.max_hp
    
    def get_hp(self) -> int:
        return self.hp
    
    def get_hp_regen(self) -> int:
        return self.hp_regen
    
    def get_max_mp(self) -> int:
        return self.max_mp
    
    def get_mp(self) -> int:
        return self.mp
    
    def get_mp_regen(self) -> int:
        return self.mp_regen
    
    def get_max_stamina(self) -> int:
        return self.max_stamina
    
    def get_stamina(self) -> int:
        return self.stamina
    
    def get_stamina_regen(self) -> int:
        return self.stamina_regen
    
    def set_max_hp(self, max_hp: int) -> None:
        self.max_hp = max_hp
    
    def set_hp(self, hp: int) -> None:
        self.hp = hp

    def set_hp_regen(self, hp_regen: int) -> None:
        self.hp_regen = hp_regen

    def set_max_mp(self, max_mp: int) -> None:
        self.max_mp = max_mp

    def set_mp(self, mp: int) -> None:
        self.mp = mp

    def set_mp_regen(self, mp_regen: int) -> None:
        self.mp_regen = mp_regen

    def set_max_stamina(self, max_stamina: int) -> None:
        self.max_stamina = max_stamina

    def set_stamina(self, stamina: int) -> None:
        self.stamina = stamina

    def set_stamina_regen(self, stamina_regen: int) -> None:
        self.stamina_regen = stamina_regen

    def remove_hp(self, hp: int) -> None:
        self.hp -= hp
        if self.hp <= 0:
            self.hp = 0

    def remove_mp(self, mp: int) -> bool:
        if self.mp < mp:
            return False
        self.mp -= mp
        return True

    def remove_stamina(self, stamina: int) -> bool:
        if self.stamina < stamina:
            return False
        self.stamina -= stamina
        return True