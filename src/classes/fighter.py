from typing import Optional
from ..interfaces.effect_protocol import IEffect
from ..interfaces.skill_protocol import ISkill

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
        
        self.effects = []
        self.skills: dict[str, ISkill] = {}

    def update(self) -> None:
        self.execute_effects()
        self.hp = min(self.hp, self.max_hp)
        self.mp = min(self.mp, self.max_mp)
        self.stamina = min(self.stamina, self.max_stamina)

    def execute_effects(self) -> None:
        for effect_item in self.effects:
            effect_item["effect"].execute(self)
            effect_item["duration"] -= 1

            if effect_item["duration"] <= 0:
                self.effects.remove(effect_item)

    def apply_effect(self, effect: IEffect) -> None:
        effect_item = {"effect": effect, "duration": effect.get_duration()}
        self.effects.append(effect_item)

    def use_skill(self, skill_name: str, target: 'Fighter') -> None:
        skill = self.get_skill(skill_name)
        if skill is None:
            return
        
        skill.use(target=target)

    def skill_usable(self, skill_name: str) -> bool:
        skill = self.get_skill(skill_name)
        if skill is None:
            return False
        
        return skill.is_usable()
    
    def add_skill(self, skill: ISkill) -> None:
        self.skills[skill.get_name()] = skill
    
    def get_skill(self, skill_name: str) -> Optional[ISkill]:
        return self.skills.get(skill_name, None)

    def has_skill(self, skill_name: str) -> bool:
        return self.get_skill(skill_name) is not None
    
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