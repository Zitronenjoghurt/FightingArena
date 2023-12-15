from typing import Optional, Protocol
from ..interfaces.fighter_protocol import IFighter

class ITeamManager(Protocol):
    # region CACHED STATE HANDLING
    def update_cached_state(self) -> None:
        ...

    def update_fighers_list(self) -> None:
        ...

    def update_team_names(self) -> None:
        ...
    
    def update_team_opponents(self) -> None:
        ...

    def update_team_count(self) -> None:
        ...
    # endregion


    # region GAME TICK UPDATES
    def update(self) -> None:
        ...

    def sort_fighters_by_initiative(self) -> None:
        ...
    # endregion
        
    
    # region CORE FUNCTIONALITY
    def is_ready(self) -> bool:
        ...
    # endregion


    # region FIGHTER MANAGEMENT
    def add_fighter(self, fighter: IFighter, team_name: str) -> None:
        ...

    def add_fighters(self, fighters: list[IFighter], team_name: str) -> None:
        ...
    # endregion


    # region DATA ACCESS
    def get_fighters(self) -> list[IFighter]:
        ...
    
    def get_fighter_opponents(self, fighter: IFighter) -> list[IFighter]:
        ...

    def get_teams(self) -> dict[str, list[IFighter]]:
        ...
    
    def get_team_count(self) -> int:
        ...

    def get_team_names(self) -> list[str]:
        ...
    
    def get_team_fighters(self, team_name: str) -> list[IFighter]:
        ...
    
    def get_team_opponents(self, team_name: str) -> list[IFighter]:
        ...

    def get_roster_string(self) -> str:
        ...
    # endregion