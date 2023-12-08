from typing import Optional, Protocol
from ..interfaces.fighter_protocol import IFighter

class IGameManager(Protocol):
    @staticmethod
    def get_instance(teams: dict[str, list[IFighter]] = {}) -> 'IGameManager':
        ...

    @staticmethod
    def reset_instance() -> None:
        ...

    def start_game(self) -> None:
        ...

    def run(self) -> None:
        ...

    def run_fighter_turn(self, fighter: IFighter) -> None:
        ...

    def check_win_condition(self) -> set[str]:
        ...

    def finish_game(self, team_name: str) -> None:
        ...

    def stop_game(self) -> None:
        ...

    def is_tie(self) -> bool:
        ...

    def get_winner_teams(self) -> list[str]:
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