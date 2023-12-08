import random
from typing import Optional
from .game_manager import GameManager
from ..interfaces.fighter_protocol import IFighter
from ..interfaces.skill_protocol import ISkill

class AIBehavior():
    def __init__(self, fighter: IFighter) -> None:
        self.fighter = fighter

    def select_skill_and_opponent(self) -> tuple[Optional[ISkill], Optional[IFighter]]:
        skill = self.select_random_skill()
        opponent = self.select_random_opponent()
        return skill, opponent
    
    def select_random_skill(self) -> Optional[ISkill]:
        usable_skills = self.fighter.get_usable_skills()
        if len(usable_skills) == 0:
            return None
        
        skill = random.choice(usable_skills)
        return skill

    def select_random_opponent(self) -> Optional[IFighter]:
        gm = GameManager.get_instance()
        opponents = gm.get_opponents(self.fighter)
        if len(opponents) == 0:
            return None

        opponent = random.choice(opponents)
        return opponent

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