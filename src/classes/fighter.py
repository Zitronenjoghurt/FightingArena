class Fighter():
    def __init__(self,
                 max_hp: int = 0,
                 max_mp: int = 0,
                 max_stamina: int = 0
                 ) -> None:
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.max_mp = max_mp
        self.mp = self.max_mp
        self.max_stamina = max_stamina
        self.stamina = self.max_stamina

    def update(self) -> None:
        self.hp = min(self.hp, self.max_hp)
        self.mp = min(self.mp, self.max_mp)
        self.stamina = min(self.stamina, self.max_stamina)

    def get_max_hp(self) -> int:
        return self.max_hp
    
    def get_hp(self) -> int:
        return self.hp
    
    def get_max_mp(self) -> int:
        return self.max_mp
    
    def get_mp(self) -> int:
        return self.mp
    
    def get_max_stamina(self) -> int:
        return self.max_stamina
    
    def get_stamina(self) -> int:
        return self.stamina
    
    def set_max_hp(self, max_hp: int) -> None:
        self.max_hp = max_hp
    
    def set_hp(self, hp: int) -> None:
        self.hp = hp

    def set_max_mp(self, max_mp: int) -> None:
        self.max_mp = max_mp

    def set_mp(self, mp: int) -> None:
        self.mp = mp

    def set_max_stamina(self, max_stamina: int) -> None:
        self.max_stamina = max_stamina

    def set_stamina(self, stamina: int) -> None:
        self.stamina = stamina

    def add_hp(self, hp: int) -> None:
        self.hp += hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def add_mp(self, mp: int) -> None:
        self.mp += mp
        if self.mp > self.max_mp:
            self.mp = self.max_mp

    def add_stamina(self, stamina: int) -> None:
        self.stamina += stamina
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina

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