from src.classes.fighter import Fighter
from src.classes.game_manager import GameManager

barbarian = Fighter.load_from_file("debug_barbarian", "Barbarian")
wizard = Fighter.load_from_file("debug_wizard", "Wizard")
teams = {"A": [barbarian], "B": [wizard]}

gm = GameManager.get_instance(teams=teams, max_rounds=10, round_time=0, print_log=True, output_log=True)
gm.start_game()