import time
from typing import Optional
from ..interfaces.fighter_protocol import IFighter

class GameManager():
    _instance = None
    
    def __init__(self, teams: dict[str, list[IFighter]] = {}, round_time: float = 1, max_rounds: int = 100000) -> None:
        if GameManager._instance is not None:
            return
        
        self.teams: dict[str, list[IFighter]] = {}
        self.running = False
        self.round = 0
        self.max_rounds = max_rounds
        self.round_time = round_time

        self.add_teams(teams=teams)

    @staticmethod
    def get_instance(teams: dict[str, list[IFighter]] = {}) -> 'GameManager':
        if not GameManager._instance:
            GameManager._instance = GameManager(teams=teams)
        return GameManager._instance
    
    @staticmethod
    def reset_instance() -> None:
        GameManager._instance = None

    def start_game(self) -> None:
        print("====={FIGHT START}=====")
        for team_name, fighters in self.teams.items():
            print(f"Team {team_name}: " + ",".join([fighter.get_name() for fighter in fighters]))
        print("====={FIGHT START}=====")
        
        self.running = True
        while self.running and self.round <= self.max_rounds:
            self.round += 1
            self.run()
            time.sleep(self.round_time)

    def run(self) -> None:
        print(f"\nROUND {self.round}:")
        fighters = self.get_fighters()

        for fighter in fighters:
            self.run_fighter_turn(fighter)
        
        for fighter in fighters:
            effect_messages = fighter.update()
            for message in effect_messages:
                print(message)

        print("==========")

        for fighter in fighters:
            print(fighter.get_status())
        
        print("==========")

        self.check_win_condition()

        time.sleep(self.round_time)

    def run_fighter_turn(self, fighter: IFighter) -> None:
        skill, opponent = fighter.get_next_move()

        if not skill:
            print(f"{fighter.get_name()} has no usable skill.")
            return
        
        if not opponent:
            print(f"{fighter.get_name()} has no opponent.")
            return
        
        success, message = skill.use(target=opponent)
        print(message)

    def check_win_condition(self) -> None:
        for fighter in self.get_fighters():
            opponents = self.get_opponents(fighter)
            if len(opponents) == 0:
                self.finish_game(self.get_fighter_team(fighter))

    def finish_game(self, team_name: str) -> None:
        print(f"\nTEAM {team_name} WINS!!!")
        self.stop_game()

    def stop_game(self) -> None:
        self.running = False

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

    def get_fighter_team(self, fighter: IFighter) -> Optional[str]:
        for team_name, fighters in self.teams.items():
            if fighter in fighters:
                return team_name
        return None

    def get_fighters(self) -> list[IFighter]:
        fighters = []
        for fighter_list in self.teams.values():
            fighters.extend(fighter_list)
        return fighters
    
    def get_opponents(self, fighter: IFighter) -> list[IFighter]:
        fighter_team = self.get_fighter_team(fighter)
        opponents = [fighter for team_name, fighters in self.teams.items() if team_name != fighter_team for fighter in fighters if fighter.get_hp() > 0]
        return opponents