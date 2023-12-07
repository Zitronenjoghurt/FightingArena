import random
from typing import Optional
from .game_manager import GameManager
from ..interfaces.fighter_protocol import IFighter
from ..interfaces.skill_protocol import ISkill

class AIBehavior():
    def __init__(self, fighter: IFighter) -> None:
        self.fighter = fighter

    def select_skill_and_opponent(self) -> tuple[ISkill, IFighter]:
        skill = self.select_random_skill()
        opponent = self.select_random_opponent()
        return skill, opponent
    
    def select_random_skill(self) -> Optional[ISkill]:
        skills = random.choice([self.fighter.get_usable_skills()])
        if len(skills) == 0:
            return None
        return skills[0]

    def select_random_opponent(self) -> Optional[IFighter]:
        gm = GameManager.get_instance()
        opponents = random.choice([gm.get_opponents(self.fighter)])
        if len(opponents) == 0:
            return None
        return opponents[0]

class SimpleAIBehavior(AIBehavior):
    pass

class AIBehaviorFactory():
    _register = {
        "random": AIBehavior,
        "simple": SimpleAIBehavior
    }

    @staticmethod
    def create_behavior(behavior_name: str, fighter: IFighter) -> AIBehavior:
        behavior_class = AIBehaviorFactory._register.get(behavior_name, None)

        if not behavior_class:
            behavior_class = AIBehavior
        
        return AIBehavior(fighter=fighter)