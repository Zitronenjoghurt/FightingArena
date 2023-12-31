from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from ..classes.game_manager import GameManager
from ..classes.team_manager import TeamManager

def worker(fight_slice, team_manager: TeamManager, max_rounds_per_fight):
    local_wins = {team_name: 0 for team_name in team_manager.get_team_names()}
    local_wins["ties"] = 0

    for _ in fight_slice:
        tm_copy = deepcopy(team_manager)
        GameManager.reset_instance()
        gm = GameManager.get_instance(team_manager=tm_copy, round_time=0, max_rounds=max_rounds_per_fight, print_log=False, output_log=False)
        gm.start_game()

        if gm.is_tie():
            local_wins["ties"] += 1
        else:
            for winner in gm.get_winner_teams():
                local_wins[winner] += 1
    return local_wins

def analyze_win_rates(team_manager: TeamManager, fight_count, max_rounds_per_fight, process_count):
    fights_per_process = fight_count // process_count
    fight_slices = [(range(i * fights_per_process, (i + 1) * fights_per_process)) for i in range(process_count)]
    
    with ProcessPoolExecutor(max_workers=process_count) as executor:
        futures = [executor.submit(worker, slice, team_manager, max_rounds_per_fight) for slice in fight_slices]

        # Aggregate results
        total_wins = {team_name: 0 for team_name in team_manager.get_team_names()}
        total_wins["ties"] = 0
        for future in as_completed(futures):
            local_wins = future.result()
            for key, value in local_wins.items():
                total_wins[key] += value

    return {team_name: str(round((win_count / fight_count) * 100, 2)) + "%" for team_name, win_count in total_wins.items()}