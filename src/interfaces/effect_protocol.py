from typing import Protocol

class IEffect(Protocol):
    def execute(self, target: object) -> str:
        ...

    def get_duration(self) -> int:
        ...

    def get_categories(self) -> list[str]:
        ...

    def get_name(self) -> str:
        ...