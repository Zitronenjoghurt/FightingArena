from typing import Optional, Protocol
from .body_protocol import IBody
from .effect_protocol import IEffect
from .skill_protocol import ISkill

class IFighter(Protocol):
    # region INITIALIZATION
    def validate_init_parameters(self, max_hp: int, max_mp: int, max_stamina: int, initiative: int, name: str, behavior_name: str) -> tuple[bool, str]:
        ...

    @staticmethod
    def load_from_file(fighter_class_name: str, fighter_name: str = "no_name") -> 'IFighter':
        ...

    @staticmethod
    def create_from_dict(data: dict) -> 'IFighter':
        ...
    # endregion
    

    # region CORE FUNCTIONALITY
    def update(self) -> None:
        ...

    def get_status(self) -> list[str]:
        ...
    
    def get_next_move(self) -> tuple[Optional[ISkill], Optional['IFighter']]:
        ...
    # endregion


    # region EFFECTS
    def execute_effects(self) -> None:
        ...

    def apply_effect(self, effect: IEffect) -> None:
        ...

    def has_effect(self, effect_name: str) -> bool:
        ...
    
    def has_effects(self, effect_names: list[str]) -> bool:
        ...

    def get_effects(self) -> list[str]:
        ...
    
    # endregion


    # region SKILLS
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
    
    def update_usable_skills(self) -> None:
        ...

    def has_skill(self, skill_name: str) -> bool:
        ...
    # endregion
    

    # region ATTACK
    def can_attack(self) -> bool:
        ...
    
    def allow_attack(self) -> None:
        ...

    def disallow_attack(self) -> None:
        ...

    def has_attacked(self) -> bool:
        ...

    def set_has_attacked(self, has_attacked: bool) -> None:
        ...
    # endregion
    
    
    # region BODY
    def add_body(self, body: IBody) -> None:
        ...
    # endregion

    # region GETTER/SETTER
    def get_name(self) -> str:
        ...
    
    def get_team(self) -> str:
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
    
    def get_initiative(self) -> int:
        ...
    
    def set_name(self, name: str) -> None:
        ...
    
    def set_team(self, team_name: str) -> None:
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

    def set_initiative(self, initiative: int) -> None:
        ...
    # endregion
        
    
    # region STAT MODIFICATION
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
    
    def apply_stat_differences(self) -> None:
        ...
    # endregion