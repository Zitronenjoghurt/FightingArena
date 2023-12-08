from typing import Protocol
from .fighter_protocol import IFighter

class IAction(Protocol):
    def execute(self, target: IFighter) -> bool:
        ...

    def is_executable(self) -> bool:
        ...

    def get_categories(self) -> list[str]:
        ...

    def add_user(self, fighter: IFighter) -> None:
        ...