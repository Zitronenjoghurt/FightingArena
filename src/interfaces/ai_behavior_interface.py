from typing import Protocol
from .fighter_protocol import IFighter
from .skill_protocol import ISkill

class IAIBehavior(Protocol):
    def select_skill_and_opponent(self) -> tuple[ISkill, IFighter]:
        ...
    
    def select_random_skill(self) -> ISkill:
        ...

    def select_random_opponent(self) -> IFighter:
        ...