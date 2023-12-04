from typing import Protocol
from .fighter_protocol import IFighter

class IEffect():
    def execute(self, target: IFighter) -> None:
        ...

    def get_duration(self) -> int:
        ...