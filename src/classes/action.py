from typing import Optional

from ..interfaces.fighter_protocol import IFighter

class Action():
    categories = []
    
    def __init__(self, user: Optional[IFighter] = None, mp_cost: int = 0, stamina_cost: int = 0) -> None:
        self.user = user
        self.mp_cost = mp_cost
        self.stamina_cost = stamina_cost

    def execute(self, target: IFighter) -> bool:
        return True

    def is_executable(self) -> bool:
        return True
    
    def remove_costs(self) -> None:
        if self.user is None:
            return
        self.user.remove_mp(self.mp_cost)
        self.user.remove_stamina(self.stamina_cost)

    def has_costs(self) -> bool:
        if self.user is None:
            return False
        return self.user.get_mp() >= self.mp_cost and self.user.get_stamina() >= self.stamina_cost
    
    def get_categories(self) -> list[str]:
        return self.categories
    
    def add_user(self, fighter: IFighter) -> None:
        self.user = fighter

class AttackAction(Action):
    categories = ["damage"]

    def __init__(self, user: Optional[IFighter] = None, damage: int = 0, mp_cost: int = 0, stamina_cost: int = 0) -> None:
        super().__init__(user, mp_cost, stamina_cost)
        self.damage = damage

    def execute(self, target: IFighter) -> bool:
        if not self.is_executable():
            return False
        target.remove_hp(self.damage)
        super().remove_costs()
        return True

    def is_executable(self) -> bool:
        if self.user is None:
            return False
        return super().has_costs()

class HealAction(Action):
    categories = ["hp_regen"]

    def __init__(self, user: Optional[IFighter] = None, amount: int = 0, mp_cost: int = 0, stamina_cost: int = 0):
        super().__init__(user, mp_cost, stamina_cost)
        self.amount = amount

    def execute(self, target: IFighter) -> bool:
        if not self.is_executable():
            return False
        target.add_hp(self.amount)
        super().remove_costs()
        return True

    def is_executable(self) -> bool:
        if self.user is None:
            return False
        return super().has_costs()
    
class LifeStealAction(Action):
    categories = ["damage", "hp_regen"]

    def __init__(self, user: Optional[IFighter] = None, damage: int = 0, heal: int = 0, damage_is_heal: bool = False, heal_multiplier: float = 1, mp_cost: int = 0, stamina_cost: int = 0) -> None:
        super().__init__(user, mp_cost, stamina_cost)
        self.damage = damage
        self.heal = heal

        if damage_is_heal:
            self.heal = round(damage * heal_multiplier)
    
    def execute(self, target: IFighter) -> bool:
        if not self.is_executable():
            return False
        target.remove_hp(self.damage)
        self.user.add_hp(self.heal)
        super().remove_costs()
        return True

    def is_executable(self) -> bool:
        if self.user is None:
            return False
        return super().has_costs()
    
class ActionFactory():
    registry = {
        "attack": AttackAction,
        "heal": HealAction,
        "lifesteal": LifeStealAction
    }

    @staticmethod
    def create_action(action_type: str, action_args: dict, user: Optional[IFighter] = None) -> Action:
        ActionClass = ActionFactory.registry.get(action_type, None)

        if ActionClass is None:
            raise ValueError(f"Action type {action_type} not found")
        try:
            action = ActionClass(user, **action_args)
        except TypeError:
            raise ValueError(f"Invalid arguments for action type {action_type}")
        
        return action