from typing import Mapping, Optional, Protocol, Sequence
from ..interfaces.fighter_protocol import IFighter

class IGameManager(Protocol):
    # region SINGLETON MANAGEMENT
    @staticmethod
    def get_instance(teams: Mapping[str, Sequence[IFighter]] = {}, round_time: float = 1, max_rounds: int = 100000, print_log: bool = True, output_log: bool = False) -> 'IGameManager':
        ...
    
    @staticmethod
    def reset_instance() -> None:
        ...
    # endregion
        
    
    # region GAME FLOW CONTROL
    def start_game(self) -> None:
        ...

    def run(self) -> None:
        ...

    def stop_game(self) -> None:
        ...

    def finish_game(self, team_names: set[str]) -> None:
        ...

    def check_win_condition(self) -> set[str]:
        ...
    
    def is_tie(self) -> bool:
        ...
    
    def get_winner_teams(self) -> list[str]:
        ...

    # endregion

    
    # region ROUND MANAGEMENT
    def run_fighter_turn(self, fighter: IFighter) -> None:
        ...

    def get_round_message(self, round: int) -> str:
        ...   

    def print_round(self, round: int) -> None:
        ...
    # endregion
        
    
    # region TEAM MANAGEMENT
    def add_teams(self, teams: Mapping[str, Sequence[IFighter]]) -> None:
        ...

    def get_team_name(self, fighter: IFighter) -> Optional[str]:
        ...

    def get_team_names(self) -> list[str]:
        ...
    
    def get_team_fighters(self, team_name: str) -> list[IFighter]:
        ...
    # endregion

    
    # region FIGHTER MANAGEMENT
    def get_fighters(self) -> list[IFighter]:
        ...
    
    def get_opponents(self, fighter: IFighter) -> list[IFighter]:
        ...
    # endregion


    # region LOGGING
    def get_start_message(self) -> str:
       ...
    
    def log_output_txt(self) -> None:
        ...

    def log_message(self, log_type: str, message: str | list) -> None:
       ...
    # endregion