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

class SkillLibrary():
    library = None
    
    def __init__(self) -> None:
        if self.library is None:
            self.library = self.__load_from_file()
    
    @staticmethod
    def __load_from_file() -> dict:
        with open(SKILLS_FILE_PATH, 'r') as f:
            data = json.load(f)
        return data
    
    def get_skill_data(self, skill_name: str) -> Optional[dict]:
        if not self.library:
            raise RuntimeError("Skill library is not loaded")
        
        return self.library.get(skill_name, None)

class Skill():
    def __init__(self, name: str, user: Optional[IFighter] = None, actions: Optional[dict[dict]] = None, effects: Optional[dict[dict]] = None, message: str = "") -> None:
        if actions is None:
            actions = {}
        if effects is None:
            effects = {}

        self.name = name
        self.message = message
        self.user: Optional[IFighter] = user
        self.categories = []

        self.actions: list[IAction] = []
        for action_type, action_args in actions.items():
            action = ActionFactory.create_action(action_type=action_type, action_args=action_args, user=self.user)
            self.add_categories(action.get_categories())
            self.actions.append(action)

        self.effects: list[IEffect] = []
        for effect_type, effect_args in effects.items():
            effect = EffectFactory.create_effect(effect_type=effect_type, effect_args=effect_args)
            self.add_categories(effect.get_categories())
            self.effects.append(effect)

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

        if actions is None or effects is None or message is None:
            raise ValueError(f"Invalid data for skill {skill_name}")
        
        return Skill(name=skill_name, user=fighter, actions=actions, effects=effects, message=message)

    def use(self, target: IFighter) -> tuple[bool, str]:
        succeeded = True

        if not self.is_usable():
            succeeded = False
        else:
            for action in self.actions:
                status = action.execute(target)
                if status == False:
                    succeeded = False
            
            for effect in self.effects:
                target.apply_effect(effect)

        if succeeded:
            return True, self.message.format(user=self.user.get_name(), opponent=target.get_name())
        else:
            return False, f"{self.user.get_name()} tried to use {self.get_name()} against {target.get_name()}, but it failed."

    def is_usable(self) -> bool:
        if self.user is None:
            return False
        
        usable = True
        for action in self.actions:
            if not action.is_executable():
                usable = False
        return usable
    
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