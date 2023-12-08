from copy import deepcopy
import cProfile
import pstats
from src.classes.fighter import Fighter
from src.classes.game_manager import GameManager
from src.modules.fight_analyzer import analyze_win_rates as analyze
from src.modules.fight_analyzer_multi import analyze_win_rates as analyze_multi

barbarian = Fighter.load_from_file("barbarian", "Barbarian")
wizard = Fighter.load_from_file("wizard", "Wizard")
teams = {"A": [barbarian], "B": [wizard]}

def profile_balancing_analyzer():
    analyze_multi(teams=teams, fight_count=100000, max_rounds_per_fight=100, process_count=10)

def profile_fights():
    for i in range(1000):
        GameManager.reset_instance()
        team_copy = deepcopy(teams)
        gm = GameManager.get_instance(teams=team_copy, round_time=0, max_rounds=100, print_log=False, output_log=False)
        gm.start_game()

def profile_performance():
    profiler = cProfile.Profile()
    profiler.enable()
    # add profile function here
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()

if __name__ == "__main__":
    gm = GameManager.get_instance(teams=teams, max_rounds=50, round_time=0, print_log=True, output_log=True)
    gm.start_game()