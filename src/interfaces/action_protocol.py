from typing import Protocol
from .fighter_protocol import IFighter

class IAction(Protocol):
    def execute(self, target: IFighter) -> None:
        ...

    def is_executable(self) -> bool:
        ...
    
    def remove_costs(self) -> None:
        ...