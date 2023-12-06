from typing import Optional
from ..interfaces.fighter_protocol import IFighter

class GameManager():
    _instance = None
    
    def __init__(self, teams: dict[str, list[IFighter]] = {}) -> None:
        if GameManager._instance is not None:
            return
        
        self.teams: dict[str, list[IFighter]] = {}
        self.running = False
        self.round = 0

        self.add_teams(teams=teams)

    @staticmethod
    def get_instance(teams: dict[str, list[IFighter]] = {}) -> 'GameManager':
        if not GameManager._instance:
            GameManager._instance = GameManager(teams=teams)
        return GameManager._instance
    
    @staticmethod
    def reset_instance() -> None:
        GameManager._instance = None

    def add_teams(self, teams: dict[str, list[IFighter]]) -> None:
        for team, fighters in teams.items():
            if self.teams.get(team, None) is None:
                self.teams[team] = fighters
            else:
                self.teams[team].extend(fighters)

    def get_team_name(self, fighter: IFighter) -> Optional[str]:
        for team_name, fighters in self.teams.items():
            if fighter in fighters:
                return team_name
        return None

    def get_team_names(self) -> list[str]:
        return list(self.teams.keys())
    
    def get_team_fighters(self, team_name: str) -> list[IFighter]:
        return self.teams.get(team_name, [])

    def get_fighters(self) -> list[IFighter]:
        fighters = []
        for fighter_list in self.teams.values():
            fighters.extend(fighter_list)
        return fighters