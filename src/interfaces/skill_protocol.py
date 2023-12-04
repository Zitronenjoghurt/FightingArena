from typing import Protocol
from .fighter_protocol import IFighter

class ISkill(Protocol):
    @staticmethod
    def create_skill(skill_name: str, fighter: IFighter) -> 'ISkill':
        ...

    def use(self, target: IFighter) -> None:
        ...

    def is_usable(self) -> bool:
        ...