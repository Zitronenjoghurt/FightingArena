import random
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
    
    def select_random_skill(self) -> ISkill:
        return random.choice([self.fighter.get_skills()])

    def select_random_opponent(self) -> IFighter:
        gm = GameManager.get_instance()
        return random.choice([gm.get_opponents(self.fighter)])

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