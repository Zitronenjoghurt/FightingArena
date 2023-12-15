from src.classes.fighter import Fighter
from src.classes.game_manager import GameManager

barbarian = Fighter.load_from_file("barbarian", "Barbarian")
wizard = Fighter.load_from_file("wizard", "Wizard")

if __name__ == "__main__":
    gm = GameManager.get_instance(max_rounds=50, round_time=0, print_log=True, output_log=True)
    gm.add_fighter(fighter=barbarian, team_name="A")
    gm.add_fighter(fighter=wizard, team_name="B")
    gm.start_game()