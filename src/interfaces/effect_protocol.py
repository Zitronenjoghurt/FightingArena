from typing import Protocol

class IEffect(Protocol):
    def execute(self, target: object) -> str:
        ...

    def on_apply(self, target: object) -> None:
        ...

    def on_remove(self) -> None:
        ...

    def get_duration(self) -> int:
        ...

    def get_categories(self) -> list[str]:
        ...

    def get_name(self) -> str:
        ...