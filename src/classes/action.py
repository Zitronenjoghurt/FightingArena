from ..interfaces.fighter_protocol import IFighter

class Action():
    def execute(self, target: IFighter) -> None:
        pass

    def is_executable(self) -> bool:
        return True
    
    def remove_costs(self) -> None:
        self.user.remove_mp(self.mp_cost)
        self.user.remove_stamina(self.stamina_cost)

class AttackAction(Action):
    def __init__(self, user: IFighter, damage: int = 0, mp_cost: int = 0, stamina_cost: int = 0) -> None:
        self.user = user
        self.damage = damage
        self.mp_cost = mp_cost
        self.stamina_cost = stamina_cost

    def execute(self, target: IFighter) -> None:
        target.remove_hp(self.damage)
        super().remove_costs()

    def is_executable(self) -> bool:
        return self.user.get_mp() >= self.mp_cost and self.user.get_stamina() >= self.stamina_cost

class HealAction(Action):
    def __init__(self, user: IFighter, amount: int = 0, mp_cost: int = 0, stamina_cost: int = 0):
        self.user = user
        self.amount = amount
        self.mp_cost = mp_cost
        self.stamina_cost = stamina_cost

    def execute(self, target: IFighter):
        target.add_hp(self.amount)
        super().remove_costs()

    def is_executable(self) -> bool:
        return self.user.get_mp() >= self.mp_cost and self.user.get_stamina() >= self.stamina_cost
    
class ActionFactory():
    registry = {
        "attack": AttackAction,
        "heal": HealAction
    }

    @staticmethod
    def create_action(action_type: str, action_args: dict, user: IFighter) -> Action:
        ActionClass = ActionFactory.registry.get(action_type, None)

        if ActionClass is None:
            raise ValueError(f"Action type {action_type} not found")
        try:
            action = ActionClass(user, **action_args)
        except TypeError:
            raise ValueError(f"Invalid arguments for action type {action_type}")
        
        return action