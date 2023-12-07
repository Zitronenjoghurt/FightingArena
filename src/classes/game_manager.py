import time
from typing import Optional
from ..interfaces.fighter_protocol import IFighter

class GameManager():
    _instance = None

    LOG_EFFECT_APPLY = "effect_apply"
    LOG_EFFECT_EXECUTE = "effect_execute"
    LOG_EFFECT_REMOVE = "effect_remove"
    LOG_FIGHTER_STATUS = "fighter_status"
    LOG_SKILL_USE = "skill_use"
    
    def __init__(self, teams: dict[str, list[IFighter]] = {}, round_time: float = 1, max_rounds: int = 100000) -> None:
        if GameManager._instance is not None:
            return
        
        self.teams: dict[str, list[IFighter]] = {}
        self.running = False
        self.round = 0
        self.max_rounds = max_rounds
        self.round_time = round_time
        self.log = GameLog()

        self.add_teams(teams=teams)

    @staticmethod
    def get_instance(teams: dict[str, list[IFighter]] = {}, round_time: float = 1, max_rounds: int = 100000) -> 'GameManager':
        if not GameManager._instance:
            GameManager._instance = GameManager(teams=teams, round_time=round_time, max_rounds=max_rounds)
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
        fighters = self.get_fighters()

        for fighter in fighters:
            self.run_fighter_turn(fighter)
        
        for fighter in fighters:
            fighter.update()

        for fighter in fighters:
            self.log_message(self.LOG_FIGHTER_STATUS, fighter.get_status())

        self.print_round(self.round)
        self.check_win_condition()

    def run_fighter_turn(self, fighter: IFighter) -> None:
        skill, opponent = fighter.get_next_move()

        if not skill:
            message = f"{fighter.get_name()} has no usable skill."
            self.log_message(self.LOG_SKILL_USE, message)
            return
        
        if not opponent:
            message = f"{fighter.get_name()} has no opponent."
            self.log_message(self.LOG_SKILL_USE, message)
            return
        
        success, message = skill.use(target=opponent)
        self.log_message(self.LOG_SKILL_USE, message=message)

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

    def print_round(self, round: int) -> None:
        print(f"\nROUND {round}:")
        self.log.print_logs(round, [self.LOG_SKILL_USE, self.LOG_EFFECT_APPLY, self.LOG_EFFECT_EXECUTE, self.LOG_EFFECT_REMOVE])
        print("==========")
        self.log.print_logs(round, [self.LOG_FIGHTER_STATUS])
        print("==========")

    def log_message(self, log_type: str, message: str) -> None:
        self.log.log_message(round=self.round, log_type=log_type, message=message)

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
    
class GameLog():
    def __init__(self) -> None:
        self.round_logs: dict[int, dict[str, list[str]]] = {}
    
    def log_message(self, round: int, log_type: str, message: str) -> None:
        if round not in self.round_logs:
            self.round_logs[round] = {}

        if log_type not in self.round_logs[round]:
            self.round_logs[round][log_type] = []

        self.round_logs[round][log_type].append(message)

    def print_logs(self, round: int, log_types: list[str]) -> None:
        if round not in self.round_logs:
            return
        
        round_log = self.get_round_log(round=round)
        for log_type in log_types:
            if log_type not in round_log:
                continue
            self.print_strings(round_log.get(log_type, []))
        
    def get_round_log(self, round: int) -> dict[str, list[str]]:
        return self.round_logs.get(round, {})
    
    def print_strings(self, strings: list[str]) -> None:
        for string in strings:
            print(string)