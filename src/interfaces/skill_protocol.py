from typing import Protocol

class ISkill(Protocol):
    @staticmethod
    def create_skill(skill_name: str, fighter) -> 'ISkill':
        ...

    def use(self, target) -> tuple[bool, str]:
        ...

    def is_usable(self) -> bool:
        ...

    def get_name(self) -> str:
        ...

    def get_categories(self) -> list[str]:
        ...

    def add_categories(self, categories: list[str]) -> None:
        ...

    def add_user(self, user) -> None:
        ...