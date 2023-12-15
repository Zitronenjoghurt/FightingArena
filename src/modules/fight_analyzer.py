from copy import deepcopy
from ..classes.game_manager import GameManager
from ..classes.team_manager import TeamManager

def analyze_win_rates(team_manager: TeamManager, fight_count: int, max_rounds_per_fight: int):
    wins = {team_name: 0 for team_name in team_manager.get_team_names()}
    wins["ties"] = 0

    for _ in range(fight_count):
        GameManager.reset_instance()
        tm_copy = deepcopy(team_manager)
        gm = GameManager.get_instance(team_manager=tm_copy, round_time=0, max_rounds=max_rounds_per_fight, print_log=False, output_log=False)
        gm.start_game()

        if gm.is_tie():
            wins["ties"] += 1
        else:
            for winner in gm.get_winner_teams():
                wins[winner] += 1

    return {team_name: str(round((win_count/fight_count)*100, 2))+"%" for team_name, win_count in wins.items()}