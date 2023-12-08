import json
import os
from typing import Optional
from .ai_behavior import AIBehavior, AIBehaviorFactory
from .game_manager import GameManager
from .skill import Skill
from ..interfaces.effect_protocol import IEffect
from ..interfaces.fighter_protocol import IFighter
from ..interfaces.skill_protocol import ISkill

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGHTERS_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'fighters')

class Fighter():
    def __init__(self,
                 max_hp: int = 0,
                 max_mp: int = 0,
                 max_stamina: int = 0,
                 name: str = "no_name",
                 behavior_name: str = "random"
                 ) -> None:
        validate_init, invalid_init_message = self.validate_init_parameters(max_hp=max_hp, max_mp=max_mp, max_stamina=max_stamina, name=name, behavior_name=behavior_name)
        if not validate_init:
            raise ValueError(f"\n====================\nInvalid init parameters for fighter {name}: {invalid_init_message}\n====================".upper())
        
        self.name = name
        self.team = ""
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.max_mp = max_mp
        self.mp = self.max_mp
        self.max_stamina = max_stamina
        self.stamina = self.max_stamina

        self.hp_difference = 0
        self.previous_hp_difference = 0
        self.mp_difference = 0
        self.previous_mp_difference = 0
        self.stamina_difference = 0
        self.previous_stamina_difference = 0
        
        self.effects = {}
        self.skills: dict[str, ISkill] = {}

        self.usable_skill_categories = []
        self.usable_category_skills: dict[str, list[ISkill]] = {}

        self.allowed_to_attack = True
        self.has_attacked_this_round = False

        self.behavior: AIBehavior = AIBehaviorFactory.create_behavior(behavior_name=behavior_name, fighter=self)

    @staticmethod
    def load_from_file(fighter_class_name: str, fighter_name: str = "no_name") -> IFighter:
        fighter_file_path = os.path.join(FIGHTERS_FILE_PATH, f"{fighter_class_name}.json")

        try:
            with open(fighter_file_path, 'r') as f:
                data = json.load(f)
                data_name = data.get("name", None)
                if not data_name or fighter_name != "no_name":
                    data["name"] = fighter_name
            return Fighter.create_from_dict(data)
        except FileNotFoundError:
            raise ValueError(f"Fighter class {fighter_class_name} does not exist. Make sure {fighter_file_path} exists.")
        except Exception as e:
            raise ValueError(f"An error occured while creating the fighter {fighter_class_name} from the file {fighter_file_path}\nLook up to the other error messages to find out more.") from e

    @staticmethod
    def create_from_dict(data: dict) -> IFighter:
        max_hp = data.get("max_hp", 0)
        max_mp = data.get("max_mp", 0)
        max_stamina = data.get("max_stamina", 0)
        skills = data.get("skills", [])
        name = data.get("name", "no_name")
        
        if not isinstance(skills, list):
            raise ValueError(f"Fighter overall skill data is invalid.\n{skills}")
        
        fighter = Fighter(max_hp=max_hp, max_mp=max_mp, max_stamina=max_stamina, name=name)

        for skill_data in skills:
            skill_name = skill_data.get("name", None)
            if skill_name is None:
                raise ValueError(f"Fighter specific skill data is invalid.\n{skill_data}")
            skill = Skill.create_skill(skill_name=skill_name, fighter=fighter)
            fighter.add_skill(skill=skill)

        fighter.update()
        return fighter
        
    def validate_init_parameters(self, max_hp: int, max_mp: int, max_stamina: int, name: str, behavior_name: str) -> tuple[bool, str]:
        if not isinstance(max_hp, int):
            return False, "max_hp has to be of type int"
        if not isinstance(max_mp, int):
            return False, "max_mphas to be of type int"
        if not isinstance(max_stamina, int):
            return False, "max_stamina has to be of type int"
        if not isinstance(name, str):
            return False, "name has to be of type string"
        if not isinstance(behavior_name, str):
            return False, "behavior_name has to be of type string"

        return True, ""

    def update(self) -> None:
        self.execute_effects()
        self.has_attacked_this_round = False
        self.apply_stat_differences()

        self.hp = min(self.hp, self.max_hp)
        self.mp = min(self.mp, self.max_mp)
        self.stamina = min(self.stamina, self.max_stamina)

        for skill in self.get_skills():
            skill.update()

        self.update_usable_skills()

    def get_next_move(self) -> tuple[Optional[ISkill], Optional[IFighter]]:
        skill, opponent = self.behavior.select_skill_and_opponent()
        
        return skill, opponent
    
    def get_status(self) -> list[str]:
        return [f"[{self.name}]", f"{self.get_hp()} ({self.previous_hp_difference})", f"{self.get_mp()} ({self.previous_mp_difference})", f"{self.get_stamina()} ({self.previous_stamina_difference})"]

    def execute_effects(self) -> None:
        if len(self.effects) == 0:
            return
        gm = GameManager.get_instance()

        remove_effects = []
        for effect_item in self.effects.values():
            message = effect_item["effect"].execute(self)
            if len(message) > 0:
                gm.log_message(gm.LOG_EFFECT_EXECUTE, message=message)
            effect_item["duration"] -= 1

            if effect_item["duration"] <= 0:
                remove_effects.append(effect_item["effect"].get_name())
        
        for effect_name in remove_effects:
            effect_item = self.effects.pop(effect_name)
            effect_item["effect"].on_remove(self)
            message = f"{self.get_name()} lost effect: {effect_name}"
            gm.log_message(gm.LOG_EFFECT_REMOVE, message=message)

    def apply_effect(self, effect: IEffect) -> None:
        gm = GameManager.get_instance()

        effect_name = effect.get_name()

        if effect_name in self.effects:
            message = f"{self.get_name()} already has effect: {effect_name}"
            gm.log_message(gm.LOG_EFFECT_APPLY, message=message)
            return

        effect_item = {"effect": effect, "duration": effect.get_duration()}
        self.effects[effect_name] = effect_item
        effect.on_apply(self)

        message = f"{self.get_name()} received effect: {effect_name}"
        gm.log_message(gm.LOG_EFFECT_APPLY, message=message)

    def has_effect(self, effect_name: str) -> bool:
        return effect_name in self.get_effects()
    
    def has_effects(self, effect_names: list[str]) -> bool:
        return not all(effect not in self.get_effects() for effect in effect_names)

    def get_effects(self) -> list[str]:
        return list(self.effects.keys())

    def use_skill(self, skill_name: str, target: IFighter) -> bool:
        skill = self.get_skill(skill_name)
        if skill is None or not self.can_attack():
            return False
        
        succeeded = skill.use(target=target)[0]
        self.set_has_attacked(succeeded)
        return succeeded

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
    
    def can_attack(self) -> bool:
        return self.allowed_to_attack
    
    def allow_attack(self) -> None:
        self.allowed_to_attack = True

    def disallow_attack(self) -> None:
        self.allowed_to_attack = False

    def has_attacked(self) -> bool:
        return self.has_attacked_this_round

    def set_has_attacked(self, has_attacked: bool) -> None:
        self.has_attacked_this_round = has_attacked
    
    def get_name(self) -> str:
        return self.name
    
    def get_team(self) -> str:
        return self.team

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
    
    def set_name(self, name: str) -> None:
        self.name = name
    
    def set_team(self, team_name: str) -> None:
        self.team = team_name

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
        self.hp_difference += hp
        if self.hp + self.hp_difference > self.max_hp:
            self.hp_difference = self.max_hp - self.hp

    def add_mp(self, mp: int) -> None:
        self.mp_difference += mp
        if self.mp + self.mp_difference > self.max_mp:
            self.mp_difference = self.max_mp - self.mp

    def add_stamina(self, stamina: int) -> None:
        self.stamina_difference += stamina
        if self.stamina + self.stamina_difference > self.max_stamina:
            self.stamina_difference = self.max_stamina - self.stamina

    def remove_hp(self, hp: int) -> None:
        self.hp_difference -= hp
        if self.hp + self.hp_difference < 0:
            self.hp_difference = -self.hp

    def remove_mp(self, mp: int) -> bool:
        if self.mp < mp:
            return False
        self.mp_difference -= mp
        return True

    def remove_stamina(self, stamina: int) -> bool:
        if self.stamina < stamina:
            return False
        self.stamina_difference -= stamina
        return True
    
    def apply_stat_differences(self) -> None:
        self.hp += self.hp_difference
        self.mp += self.mp_difference
        self.stamina += self.stamina_difference

        if self.hp < 0:
            self.set_hp(0)
        
        self.previous_hp_difference = self.hp_difference
        self.hp_difference = 0
        self.previous_mp_difference = self.mp_difference
        self.mp_difference = 0
        self.previous_stamina_difference = self.stamina_difference
        self.stamina_difference = 0