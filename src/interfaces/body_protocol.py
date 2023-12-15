from typing import Protocol

class IBody(Protocol):
    @staticmethod
    def create(body_parts_list: list[dict]) -> 'IBody':
        ...
    
    def add_fighter(self, fighter) -> None:
        ...