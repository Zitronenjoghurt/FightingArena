from typing import Optional, Protocol
from ..interfaces.fighter_protocol import IFighter

class IGameManager(Protocol):
    @staticmethod
    def get_instance(teams: dict[str, list[IFighter]] = {}) -> 'IGameManager':
        ...

    def add_teams(self, teams: dict[str, list[IFighter]]) -> None:
        ...

    def get_team_name(self, fighter: IFighter) -> Optional[str]:
        ...

    def get_team_names(self) -> list[str]:
        ...
    
    def get_team_fighters(self, team_name: str) -> list[IFighter]:
        ...

    def get_fighters(self) -> list[IFighter]:
        ...