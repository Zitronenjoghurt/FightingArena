import random
from typing import Callable, Optional
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
        opponents = gm.team_manager.get_fighter_opponents(self.fighter)
        if len(opponents) == 0:
            return None

        opponent = random.choice(opponents)
        return opponent

class SimpleAIBehavior(AIBehavior):
    HP_HEALTH_TRESHOLD = 0.5
    MP_REGEN_TRESHOLD = 0.5
    STAMINA_REGEN_TRESHOLD = 0.5

    SCORE_FUNCTIONS = {
        "hp_regen": "calculate_hp_regen_score",
        "mp_regen": "calculate_mp_regen_score",
        "stamina_regen": "calculate_stamina_regen_score"
    }

    def select_skill_and_opponent(self) -> tuple[Optional[ISkill], Optional[IFighter]]:
        skill = self.select_skill()
        opponent = self.select_random_opponent()
        return skill, opponent
    
    def select_skill(self) -> Optional[ISkill]:
        category_skills = self.fighter.get_usable_category_skills()
        categories = list(category_skills.keys())

        category_scores = {}
        for category in categories:
            score_function = self.get_score_function(category=category)
            if not score_function:
                category_scores[category] = 1
            else:
                category_scores[category] = score_function()
        
        final_categories = self.get_highest_score_categories(category_scores=category_scores)
        chosen_category = random.choice(final_categories)
        return random.choice(category_skills.get(chosen_category, []))

    def get_score_function(self, category: str) -> Optional[Callable]:
        function_name = self.SCORE_FUNCTIONS.get(category, None)

        if not function_name:
            return None
        
        return getattr(self, function_name)

    def get_highest_score_categories(self, category_scores: dict[str, int]) -> list[str]:
        if not category_scores:
            return []
        
        max_score = max(category_scores.values())

        highest_score_categories = [category for category, score in category_scores.items() if score == max_score]

        return highest_score_categories
    
    def calculate_hp_regen_score(self) -> int:
        hp_percentage = self.fighter.get_hp() / self.fighter.get_max_hp()
        if hp_percentage > self.HP_HEALTH_TRESHOLD:
            return 0
        score = (self.HP_HEALTH_TRESHOLD - hp_percentage) / self.HP_HEALTH_TRESHOLD * 1000
        return int(score)
    
    def calculate_mp_regen_score(self) -> int:
        if self.fighter.get_max_mp() == 0:
            return 0
        
        mp_percentage = self.fighter.get_mp() / self.fighter.get_max_mp()
        if mp_percentage > self.MP_REGEN_TRESHOLD:
            return 0
        
        score = (self.MP_REGEN_TRESHOLD - mp_percentage) / self.MP_REGEN_TRESHOLD * 1000
        return int(score)
    
    def calculate_stamina_regen_score(self) -> int:
        if self.fighter.get_max_stamina() == 0:
            return 0
        
        stamina_percentage = self.fighter.get_stamina() / self.fighter.get_max_stamina()
        if stamina_percentage > self.STAMINA_REGEN_TRESHOLD:
            return 0
        
        score = (self.STAMINA_REGEN_TRESHOLD - stamina_percentage) / self.STAMINA_REGEN_TRESHOLD * 1000
        return int(score)

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
        
        return behavior_class(fighter=fighter)