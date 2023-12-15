from typing import Optional
from ..interfaces.fighter_protocol import IFighter

class TeamManager():
    def __init__(self) -> None:
        self.teams: dict[str, list[IFighter]] = {}

        # Cached state properties
        self.fighters_list: list[IFighter] = []
        self.team_names: list[str] = []
        self.team_opponents: dict[str, list[IFighter]] = {}
        self.team_count: int = 0

    # region CACHED STATE HANDLING
    def update_cached_state(self) -> None:
        self.update_fighers_list()
        self.update_team_names()
        self.update_team_opponents()
        self.update_team_count()

        self.update()

    def update_fighers_list(self) -> None:
        fighters_list = []
        for fighters in self.teams.values():
            fighters_list.extend(fighters)

        self.fighters_list = fighters_list

    def update_team_names(self) -> None:
        self.team_names = list(self.teams.keys())
    
    def update_team_opponents(self) -> None:
        team_names = self.get_team_names()
        team_opponents_mapping = {team_name: [] for team_name in team_names}

        for current_team, fighters in self.teams.items():
            opponent_teams = [opponent_team for opponent_team in team_names if opponent_team != current_team]

            for opponent_team in opponent_teams:
                team_opponents_mapping[opponent_team].extend(fighters)

        self.team_opponents = team_opponents_mapping

    def update_team_count(self) -> None:
        self.team_count = len(self.get_team_names())
    # endregion


    # region GAME TICK UPDATES
    def update(self) -> None:
        self.sort_fighters_by_initiative()

    def sort_fighters_by_initiative(self) -> None:
        self.fighters_list.sort(key=lambda fighter: fighter.get_initiative(), reverse=True)
    # endregion
        
    
    # region CORE FUNCTIONALITY
    def is_ready(self) -> bool:
        return self.team_count >= 2
    # endregion


    # region FIGHTER MANAGEMENT
    def add_fighter(self, fighter: IFighter, team_name: str) -> None:
        if not fighter:
            return
        
        if self.teams.get(team_name, None) is None:
            self.teams[team_name] = []
        
        self.teams[team_name].append(fighter)
        fighter.set_team(team_name=team_name)
        self.update_cached_state()

    def add_fighters(self, fighters: list[IFighter], team_name: str) -> None:
        for fighter in fighters:
            self.add_fighter(fighter=fighter, team_name=team_name)
    # endregion


    # region DATA ACCESS
    def get_fighters(self) -> list[IFighter]:
        return self.fighters_list
    
    def get_fighter_opponents(self, fighter: IFighter) -> list[IFighter]:
        team_name = fighter.get_team()
        return self.get_team_opponents(team_name=team_name)

    def get_teams(self) -> dict[str, list[IFighter]]:
        return self.teams
    
    def get_team_count(self) -> int:
        return self.team_count

    def get_team_names(self) -> list[str]:
        return self.team_names
    
    def get_team_fighters(self, team_name: str) -> list[IFighter]:
        return self.teams.get(team_name, [])
    
    def get_team_opponents(self, team_name: str) -> list[IFighter]:
        opponents = self.team_opponents.get(team_name, [])
        return [opponent for opponent in opponents if opponent.get_hp() > 0]
    
    def get_roster_string(self) -> str:
        team_summaries = []
        for team_name, fighters in self.get_teams().items():
            members = [fighter.get_name() for fighter in fighters]
            team_summary = f"Team {team_name}: " + ', '.join(members)
            team_summaries.append(team_summary)
        return '\n'.join(team_summaries)
    # endregion