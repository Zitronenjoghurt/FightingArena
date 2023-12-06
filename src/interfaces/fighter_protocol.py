from typing import Optional, Protocol
from .effect_protocol import IEffect
from .skill_protocol import ISkill

class IFighter(Protocol):
    @staticmethod
    def load_from_file(fighter_name: str) -> 'IFighter':
        ...

    @staticmethod
    def create_from_dict(data: dict) -> 'IFighter':
        ...
        
    def validate_init_parameters(self, max_hp: int, max_mp: int, max_stamina: int) -> bool:
        ...

    def update(self) -> None:
        ...

    def execute_effects(self) -> None:
        ...

    def apply_effect(self, effect: IEffect) -> None:
        ...

    def use_skill(self, skill_name: str, target: 'IFighter') -> bool:
        ...

    def skill_usable(self, skill_name: str) -> bool:
        ...
    
    def add_skill(self, skill: ISkill) -> None:
        ...

    def add_skills(self, skills: list[ISkill]) -> None:
        ...
    
    def get_skill(self, skill_name: str) -> Optional[ISkill]:
        ...

    def get_skills(self) -> list[ISkill]:
        ...
    
    def get_usable_skills(self) -> list[ISkill]:
        ...

    def get_usable_skill_categories(self) -> list[str]:
        ...
    
    def get_usable_category_skills(self) -> dict[str, list[ISkill]]:
        ...
    
    def update_usable_skills_by_category(self) -> dict[str, list[ISkill]]:
        ...

    def has_skill(self, skill_name: str) -> bool:
        ...

    def get_max_hp(self) -> int:
        ...
    
    def get_hp(self) -> int:
        ...
    
    def get_max_mp(self) -> int:
        ...
    
    def get_mp(self) -> int:
        ...
    
    def get_max_stamina(self) -> int:
        ...
    
    def get_stamina(self) -> int:
        ...
    
    def set_max_hp(self, max_hp: int) -> None:
        ...
    
    def set_hp(self, hp: int) -> None:
        ...

    def set_max_mp(self, max_mp: int) -> None:
        ...

    def set_mp(self, mp: int) -> None:
        ...

    def set_max_stamina(self, max_stamina: int) -> None:
        ...

    def set_stamina(self, stamina: int) -> None:
        ...

    def add_hp(self, hp: int) -> None:
        ...

    def add_mp(self, mp: int) -> None:
        ...

    def add_stamina(self, stamina: int) -> None:
        ...

    def remove_hp(self, hp: int) -> None:
        ...

    def remove_mp(self, mp: int) -> bool:
        ...

    def remove_stamina(self, stamina: int) -> bool:
        ...