import json
import os

from typing import Optional
from .action import ActionFactory
from .effect import EffectFactory

from ..interfaces.action_protocol import IAction
from ..interfaces.effect_protocol import IEffect
from ..interfaces.fighter_protocol import IFighter

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'skills.json')
DEBUG_SKILLS_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'debug_skills.json')

class SkillLibrary():
    library = None
    
    def __init__(self) -> None:
        if self.library is None:
            self.library = self.__load_from_file()
    
    @staticmethod
    def __load_from_file() -> dict:
        data = {}
        with open(SKILLS_FILE_PATH, 'r') as f:
            data.update(json.load(f))
        with open(DEBUG_SKILLS_FILE_PATH, 'r') as f:
            data.update(json.load(f))
        return data
    
    def get_skill_data(self, skill_name: str) -> Optional[dict]:
        if not self.library:
            raise RuntimeError("Skill library is not loaded")
        
        return self.library.get(skill_name, None)

class Skill():
    def __init__(self, name: str, user: Optional[IFighter] = None, actions: Optional[dict[str, dict]] = None, effects: Optional[dict[str, dict]] = None, message: str = "", cooldown: int = 0, mp_cost: int = 0, stamina_cost: int = 0) -> None:
        if actions is None:
            actions = {}
        if effects is None:
            effects = {}

        validate_init, invalid_init_message = self.validate_init_parameters(name=name, message=message, cooldown=cooldown, mp_cost=mp_cost, stamina_cost=stamina_cost)
        if not validate_init:
            raise ValueError(f"\n====================\nInvalid init parameters for skill {name}: {invalid_init_message}\n====================".upper())

        self.name = name
        self.message = message
        self.user: Optional[IFighter] = user
        self.categories = []
        self.cooldown = cooldown
        self.current_cooldown = 0

        self.mp_cost = mp_cost
        self.stamina_cost = stamina_cost

        self.actions: list[IAction] = []
        try:
            for action_type, action_args in actions.items():
                action = ActionFactory.create_action(action_type=action_type, action_args=action_args, user=self.user)
                self.add_categories(action.get_categories())
                self.actions.append(action)
        except Exception as e:
            raise ValueError(f"An error occured while creating the actions for the skill {self.name}") from e

        self.effects: list[IEffect] = []
        try:
            for effect_type, effect_args in effects.items():
                effect = EffectFactory.create_effect(effect_type=effect_type, effect_args=effect_args)
                self.add_categories(effect.get_categories())
                self.effects.append(effect)
        except Exception as e:
            raise ValueError(f"An error occured while creating the effects for the skill {self.name}") from e

    @staticmethod
    def create_skill(skill_name: str, fighter: Optional[IFighter] = None) -> 'Skill':
        skill_name = skill_name.lower()
        library = SkillLibrary()
        skill = library.get_skill_data(skill_name)

        if not skill:
            raise ValueError(f"Skill {skill_name} not found")
        
        actions = skill.get("actions", None)
        effects = skill.get("effects", None)
        message = skill.get("message", None)
        cooldown = skill.get("cooldown", 0)
        mp_cost = skill.get("mp_cost", 0)
        stamina_cost = skill.get("stamina_cost", 0)

        if actions is None:
            raise ValueError(f"No actions defined for skill {skill_name}")
        
        if effects is None:
            raise ValueError(f"No effects defined for skill {skill_name}")
        
        if message is None:
            raise ValueError(f"No message defined for skill {skill_name}")
        
        try:
            skill = Skill(name=skill_name, user=fighter, actions=actions, effects=effects, message=message, cooldown=cooldown, mp_cost=mp_cost, stamina_cost=stamina_cost)
        except Exception as e:
            raise ValueError(f"An error occured while trying to create skill {skill_name}\nLook up to the other error messages to find out more.") from e
        
        return skill
    
    def validate_init_parameters(self, name: str, message: str, cooldown: int, mp_cost: int, stamina_cost: int) -> tuple[bool, str]:
        if not isinstance(name, str):
            return False, "name has to be of type string"
        if not isinstance(message, str):
            return False, "message has to be of type string"
        if not isinstance(cooldown, int):
            return False, "cooldown has to be of type int"
        if not isinstance(mp_cost, int):
            return False, "mp_cost has to be of type int"
        if not isinstance(stamina_cost, int):
            return False, "stamina_cost has to be of type int"
        
        return True, ""
    
    def update(self) -> None:
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def use(self, target: IFighter) -> tuple[bool, str]:
        user_name = "no_name"
        if self.user:
            user_name = self.user.get_name()

        if self.on_cooldown():
            return False, f"{user_name} tried to use {self.get_name()} against {target.get_name()}, but its on cooldown (how stupid, lol)."
        
        if not self.user_has_costs():
            return False, f"{user_name} tried to use {self.get_name()} against {target.get_name()}, but they dont have enough MP or Stamina (idiot)."

        succeeded = True

        if not self.is_usable():
            succeeded = False
        else:
            for action in self.actions:
                status = True
                if action.is_executable():
                    status = action.execute(target)
                if status == False:
                    succeeded = False
            
            for effect in self.effects:
                if self.user and effect.apply_on_self():
                    self.user.apply_effect(effect=effect)
                if effect.apply_on_target():
                    target.apply_effect(effect=effect)
        
        if self.cooldown > 0:
            self.current_cooldown = self.cooldown + 1

        if succeeded:
            self.user_remove_costs()
            return True, self.message.format(user=user_name, opponent=target.get_name())
        else:
            return False, f"{user_name} tried to use {self.get_name()} against {target.get_name()}, but it failed."

    def is_usable(self) -> bool:
        if self.user is None or self.on_cooldown() or not self.user_has_costs():
            return False
        
        usable = True
        for action in self.actions:
            if not action.is_executable():
                usable = False
        return usable
    
    def user_has_costs(self) -> bool:
        if self.user is None:
            return False
        
        return self.user.get_mp() >= self.mp_cost and self.user.get_stamina() >= self.stamina_cost
    
    def user_remove_costs(self) -> None:
        if self.user is None:
            return
        
        self.user.remove_mp(self.mp_cost)
        self.user.remove_stamina(self.stamina_cost)
    
    def get_current_cooldown(self) -> int:
        return self.current_cooldown
    
    def on_cooldown(self) -> bool:
        return self.current_cooldown > 0
    
    def get_name(self) -> str:
        return self.name
    
    def get_categories(self) -> list[str]:
        return self.categories
    
    def add_categories(self, categories: list[str]) -> None:
        for category in categories:
            if category not in self.categories:
                self.categories.append(category)

    def add_user(self, user: IFighter) -> None:
        self.user = user
        for action in self.actions:
            action.add_user(user)