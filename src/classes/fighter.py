import json
import os
from typing import Optional
from .ai_behavior import AIBehavior, AIBehaviorFactory
from .skill import Skill
from ..interfaces.effect_protocol import IEffect
from ..interfaces.skill_protocol import ISkill

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGHTERS_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'fighters')

class Fighter():
    def __init__(self,
                 max_hp: int = 0,
                 max_mp: int = 0,
                 max_stamina: int = 0,
                 behavior_name: str = "random"
                 ) -> None:
        if not self.validate_init_parameters(max_hp=max_hp, max_mp=max_mp, max_stamina=max_stamina):
            raise ValueError(f"Invalid init parameters for fighter class.")
        
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.max_mp = max_mp
        self.mp = self.max_mp
        self.max_stamina = max_stamina
        self.stamina = self.max_stamina
        
        self.effects = []
        self.skills: dict[str, ISkill] = {}

        self.usable_skill_categories = []
        self.usable_category_skills: dict[str, ISkill] = {}

        self.behavior: AIBehavior = AIBehaviorFactory.create_behavior(behavior_name=behavior_name, fighter=self)

    @staticmethod
    def load_from_file(fighter_name: str) -> 'Fighter':
        fighter_file_path = os.path.join(FIGHTERS_FILE_PATH, f"{fighter_name}.json")

        try:
            with open(fighter_file_path, 'r') as f:
                data = json.load(f)
            return Fighter.create_from_dict(data)
        except FileNotFoundError:
            raise ValueError(f"Fighter {fighter_name} does not exist. Make sure {fighter_file_path} exists.")

    @staticmethod
    def create_from_dict(data: dict) -> 'Fighter':
        max_hp = data.get("max_hp", None)
        max_mp = data.get("max_mp", None)
        max_stamina = data.get("max_stamina", None)
        skills = data.get("skills", None)

        if any(var is None for var in [max_hp, max_mp, max_stamina, skills]):
            raise ValueError(f"Fighter data is incomplete.")
        
        if not isinstance(skills, list):
            raise ValueError(f"Fighter overall skill data is invalid.\n{skills}")
        
        fighter = Fighter(max_hp=max_hp, max_mp=max_mp, max_stamina=max_stamina)

        for skill_data in skills:
            skill_name = skill_data.get("name", None)
            if skill_name is None:
                raise ValueError(f"Fighter specific skill data is invalid.\n{skill_data}")
            skill = Skill.create_skill(skill_name=skill_name, fighter=fighter)
            fighter.add_skill(skill=skill)

        fighter.update()
        return fighter
        
    def validate_init_parameters(self, max_hp: int, max_mp: int, max_stamina: int) -> bool:
        if any(not isinstance(var, int) for var in [max_hp, max_mp, max_stamina]):
            return False
        
        return True

    def update(self) -> None:
        self.update_usable_skills()

        self.execute_effects()
        self.hp = min(self.hp, self.max_hp)
        self.mp = min(self.mp, self.max_mp)
        self.stamina = min(self.stamina, self.max_stamina)

    def get_next_move(self) -> Optional[tuple[ISkill, 'Fighter']]:
        skill, opponent = self.behavior.select_skill_and_opponent()

        if not skill or not opponent:
            return None
        
        return skill, opponent

    def execute_effects(self) -> None:
        for effect_item in self.effects:
            effect_item["effect"].execute(self)
            effect_item["duration"] -= 1

            if effect_item["duration"] <= 0:
                self.effects.remove(effect_item)

    def apply_effect(self, effect: IEffect) -> None:
        effect_item = {"effect": effect, "duration": effect.get_duration()}
        self.effects.append(effect_item)

    def use_skill(self, skill_name: str, target: 'Fighter') -> bool:
        skill = self.get_skill(skill_name)
        if skill is None:
            return False
        
        return skill.use(target=target)

    def skill_usable(self, skill_name: str) -> bool:
        skill = self.get_skill(skill_name)
        if skill is None:
            return False
        
        return skill.is_usable()
    
    def add_skill(self, skill: ISkill) -> None:
        skill.add_user(self)
        self.skills[skill.get_name()] = skill

    def add_skills(self, skills: list[ISkill]) -> None:
        for skill in skills:
            self.add_skill(skill)
    
    def get_skill(self, skill_name: str) -> Optional[ISkill]:
        return self.skills.get(skill_name, None)
    
    def get_skills(self) -> list[ISkill]:
        return list(self.skills.values())
    
    def get_usable_skills(self) -> list[ISkill]:
        return [skill for skill in self.get_skills() if skill.is_usable()]
    
    def get_usable_skill_categories(self) -> list[str]:
        return self.usable_skill_categories
    
    def get_usable_category_skills(self) -> dict[str, list[ISkill]]:
        return self.usable_category_skills
    
    def update_usable_skills(self) -> None:
        result = {}
        for skill in self.get_usable_skills():
            for category in skill.get_categories():
                if category not in result:
                    result[category] = []
                result[category].append(skill)
        self.usable_category_skills = result
        self.usable_skill_categories = list(result.keys())

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