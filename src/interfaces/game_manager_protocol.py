from typing import Optional, Protocol
from ..interfaces.fighter_protocol import IFighter
from ..interfaces.team_manager_interface import ITeamManager

class IGameManager(Protocol):
    # region SINGLETON MANAGEMENT
    @staticmethod
    def get_instance(team_manager: Optional[ITeamManager] = None, round_time: float = 1, max_rounds: int = 100000, print_log: bool = True, output_log: bool = False) -> 'IGameManager':
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
    def add_fighter(self, fighter: IFighter, team_name: str) -> None:
        ...

    def add_fighters(self, fighters: list[IFighter], team_name: str) -> None:
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