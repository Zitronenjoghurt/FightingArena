from ..interfaces.fighter_protocol import IFighter

class Action():
    def execute(self):
        pass

    def is_executable(self) -> bool:
        return True

class AttackAction(Action):
    def __init__(self, user: IFighter, target: IFighter, damage: int):
        self.user = user
        self.target = target
        self.damage = damage

    def execute(self):
        self.target.remove_hp(self.damage)

class HealAction(Action):
    def __init__(self, user: IFighter, target: IFighter, mp_cost: int, heal_amount: int):
        self.user = user
        self.target = target
        self.mp_cost = mp_cost
        self.heal_amount = heal_amount

    def execute(self):
        self.user.remove_mp(self.mp_cost)
        self.target.add_hp(self.heal_amount)

    def is_executable(self) -> bool:
        return self.user.get_mp() >= self.mp_cost
    
class ActionFactory():
    registry = {
        "attack": AttackAction,
        "heal": HealAction
    }

    @staticmethod
    def create_action(action_type: str, action_args: dict, user: IFighter, target: IFighter,) -> Action:
        ActionClass = ActionFactory.registry.get(action_type, None)

        if ActionClass is None:
            raise ValueError(f"Action type {action_type} not found")
        try:
            action = ActionClass(user, target, **action_args)
        except TypeError:
            raise ValueError(f"Invalid arguments for action type {action_type}")
        
        return action