from typing import Protocol

class IEffect(Protocol):
    def execute(self, target: object) -> None:
        ...

    def get_duration(self) -> int:
        ...

    def get_categories(self) -> list[str]:
        ...