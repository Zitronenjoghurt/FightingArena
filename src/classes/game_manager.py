import time
from typing import Mapping, Optional, Sequence
from .team_manager import TeamManager
from ..interfaces.fighter_protocol import IFighter
from ..modules.tabularize import create_table

LOG_OUTPUT_FILE_PATH = "output.txt"

class GameManager():
    _instance = None

    LOG_DEBUG_FIGHTER_STATUS_RAW = "debug_fighter_status_raw"
    LOG_EFFECT_APPLY = "effect_apply"
    LOG_EFFECT_EXECUTE = "effect_execute"
    LOG_EFFECT_REMOVE = "effect_remove"
    LOG_GAME_STATUS_TOP = "game_status_top"
    LOG_GAME_FINISH = "game_finish"
    LOG_FIGHTER_STATUS = "fighter_status"
    LOG_SKILL_USE = "skill_use"
    
    def __init__(self, team_manager: Optional[TeamManager] = None, round_time: float = 1, max_rounds: int = 100000, print_log: bool = True, output_log: bool = False) -> None:
        if GameManager._instance is not None:
            return
        
        if team_manager is None:
            team_manager = TeamManager()
        
        self.winner_teams: list[str] = []
        self.running = False
        self.round = 0
        self.max_rounds = max_rounds
        self.round_time = round_time
        
        self.log = GameLog()
        self.print_log = print_log
        self.output_log = output_log

        self.team_manager: TeamManager = team_manager

    # region SINGLETON MANAGEMENT
    @staticmethod
    def get_instance(team_manager: Optional[TeamManager] = None, round_time: float = 1, max_rounds: int = 100000, print_log: bool = True, output_log: bool = False) -> 'GameManager':
        if not GameManager._instance:
            GameManager._instance = GameManager(team_manager=team_manager, round_time=round_time, max_rounds=max_rounds, print_log=print_log, output_log=output_log)
        return GameManager._instance
    
    @staticmethod
    def reset_instance() -> None:
        GameManager._instance = None

    # endregion
        
    
    # region GAME FLOW CONTROL
    def start_game(self) -> None:
        self.log_message(self.LOG_GAME_STATUS_TOP, "==================={FIGHT START}==================")
        self.log_message(self.LOG_GAME_STATUS_TOP, self.team_manager.get_roster_string())
        self.log_message(self.LOG_GAME_STATUS_TOP, "==================================================")
        
        if self.print_log:
            print(self.get_start_message())

        self.running = True
        while self.running and self.round <= self.max_rounds:
            self.round += 1
            self.run()
            time.sleep(self.round_time)

    def run(self) -> None:
        self.log_message(self.LOG_GAME_STATUS_TOP, f"[ROUND {self.round}]")
        fighters = self.team_manager.get_fighters()

        for fighter in fighters:
            self.run_fighter_turn(fighter)
        
        fighter_status_headers = ["Name", "HP", "MP", "Stamina"]
        fighter_statuses = []
        for fighter in fighters:
            fighter.update()
            fighter_statuses.append(fighter.get_status())

        self.team_manager.update()

        self.log_message(self.LOG_DEBUG_FIGHTER_STATUS_RAW, fighter_statuses)
        self.log_message(self.LOG_FIGHTER_STATUS, create_table(fighter_status_headers, fighter_statuses))

        winning_teams = self.check_win_condition()
        if len(winning_teams) > 0:
            self.finish_game(winning_teams)

        if self.print_log:
            self.print_round(self.round)

    def stop_game(self) -> None:
        if self.output_log:
            self.log_output_txt()
        self.running = False

    def finish_game(self, team_names: set[str]) -> None:
        win_messages = []
        for team_name in team_names:
            win_messages.append(f"TEAM {team_name} WINS!!!")
            self.winner_teams.append(team_name)
        
        if not self.is_tie():
            self.log_message(self.LOG_GAME_FINISH, message='\n'.join(win_messages))
        else:
            tie_message = f"ITS A TIE!"
            self.log_message(self.LOG_GAME_FINISH, message=tie_message)

        self.stop_game()

    def check_win_condition(self) -> set[str]:
        winning_teams = set()
        for fighter in self.team_manager.get_fighters():
            opponents = self.team_manager.get_fighter_opponents(fighter)
            if len(opponents) == 0:
                winning_teams.add(fighter.get_team())
        return winning_teams
    
    def is_tie(self) -> bool:
        return len(self.get_winner_teams()) == self.team_manager.get_team_count()
    
    def get_winner_teams(self) -> list[str]:
        return self.winner_teams
    
    # endregion

    
    # region ROUND MANAGEMENT
    def run_fighter_turn(self, fighter: IFighter) -> None:
        skill, opponent = fighter.get_next_move()

        if not fighter.can_attack():
            return

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
        if success:
            fighter.set_has_attacked(True)

    def get_round_message(self, round: int) -> str:
        round_message = [
            "==================================================",
            self.log.get_logs_string(round, [self.LOG_GAME_STATUS_TOP]),
            self.log.get_logs_string(round, [self.LOG_FIGHTER_STATUS]),
            "",
            self.log.get_logs_string(round, [self.LOG_SKILL_USE, self.LOG_EFFECT_APPLY, self.LOG_EFFECT_EXECUTE, self.LOG_EFFECT_REMOVE, self.LOG_GAME_FINISH]),
            "==================================================\n\n",
        ]
        return '\n'.join(round_message)   

    def print_round(self, round: int) -> None:
        round_message = self.get_round_message(round)
        print(round_message)

    # endregion


    # region TEAM MANAGEMENT
    def add_fighter(self, fighter: IFighter, team_name: str) -> None:
        self.team_manager.add_fighter(fighter=fighter, team_name=team_name)

    def add_fighters(self, fighters: list[IFighter], team_name: str) -> None:
        self.team_manager.add_fighters(fighters=fighters, team_name=team_name)

    # endregion

    # region LOGGING
    def get_start_message(self) -> str:
        return self.log.get_logs_string(0, [self.LOG_GAME_STATUS_TOP]) + "\n"
    
    def log_output_txt(self) -> None:
        round_messages = [self.get_start_message()]
        for i in range(1, self.round + 1):
            round_messages.append(self.get_round_message(i))
        
        log_string = '\n'.join(round_messages)
        with open(LOG_OUTPUT_FILE_PATH, "w") as file:
            file.write(log_string)

    def log_message(self, log_type: str, message: str | list) -> None:
        self.log.log_message(round=self.round, log_type=log_type, message=message)

    # endregion
    
class GameLog():
    def __init__(self) -> None:
        self.round_logs: dict[int, dict[str, list[str]]] = {}
    
    # region LOG MANAGEMENT
    def log_message(self, round: int, log_type: str, message: str | list) -> None:
        if round not in self.round_logs:
            self.round_logs[round] = {}

        if log_type not in self.round_logs[round]:
            self.round_logs[round][log_type] = []

        self.round_logs[round][log_type].append(message) # type: ignore

    def get_round_log(self, round: int) -> dict[str, list[str]]:
        return self.round_logs.get(round, {})

    def get_logs_string(self, round: int, log_types: list[str]) -> str:
        if round not in self.round_logs:
            return ""
        
        round_log = self.get_round_log(round)
        logs_strings = []
        for log_type in log_types:
            if log_type not in round_log:
                continue
            logs_strings.extend(round_log.get(log_type, []))
        return '\n'.join(logs_strings)
    
    # endregion
    

    # region PRINT
    def print_logs(self, round: int, log_types: list[str]) -> None:
        if round not in self.round_logs:
            return
        
        print(self.get_logs_string(round=round, log_types=log_types))
    
    def print_strings(self, strings: list[str]) -> None:
        for string in strings:
            print(string)
            
    # endregion