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
    def __init__(self, name: str, user: IFighter, actions: dict[dict], effects: dict[dict]) -> None:
        self.name = name
        self.user: IFighter = user

        self.actions: list[IAction] = []
        for action_type, action_args in actions.items():
            action = ActionFactory.create_action(action_type=action_type, action_args=action_args, user=self.user)
            self.actions.append(action)

        self.effects: list[IEffect] = []
        for effect_type, effect_args in effects.items():
            effect = EffectFactory.create_effect(effect_type=effect_type, effect_args=effect_args)
            self.effects.append(effect)

    @staticmethod
    def create_skill(skill_name: str, fighter: IFighter) -> 'Skill':
        skill_name = skill_name.lower()
        library = SkillLibrary()
        skill = library.get_skill_data(skill_name)

        if not skill:
            raise ValueError(f"Skill {skill_name} not found")
        
        actions = skill.get("actions", None)
        effects = skill.get("effects", None)

        if actions is None or effects is None:
            raise ValueError(f"Invalid data for skill {skill_name}")
        
        return Skill(name=skill_name, user=fighter, actions=actions, effects=effects)

    def use(self, target: IFighter) -> None:
        for action in self.actions:
            action.execute(target)
        
        for effect in self.effects:
            target.apply_effect(effect)

    def is_usable(self) -> bool:
        usable = True
        for action in self.actions:
            if not action.is_executable():
                usable = False
        return usable
    
    def get_name(self) -> str:
        return self.name