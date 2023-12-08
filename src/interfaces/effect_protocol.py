from typing import Protocol

class IEffect(Protocol):
    def execute(self, target) -> str:
        ...

    def on_apply(self, target) -> None:
        ...

    def on_remove(self, target) -> None:
        ...

    def get_duration(self) -> int:
        ...

    def get_categories(self) -> list[str]:
        ...

    def get_name(self) -> str:
        ...