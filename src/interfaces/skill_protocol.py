from typing import Protocol

class ISkill(Protocol):
    @staticmethod
    def create_skill(skill_name: str, fighter: object) -> 'ISkill':
        ...

    def use(self, target: object) -> None:
        ...

    def is_usable(self) -> bool:
        ...

    def get_name(self) -> str:
        ...