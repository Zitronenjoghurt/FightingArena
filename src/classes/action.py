from typing import Optional

from ..interfaces.fighter_protocol import IFighter

class Action():
    categories = []
    
    def __init__(self, user: Optional[IFighter] = None, on_self: bool = False, on_target: bool = False) -> None:
        self.user: Optional[IFighter] = user
        self.on_self = on_self
        self.on_target = on_target

    def execute(self, target: IFighter) -> bool:
        return True

    def is_executable(self) -> bool:
        return True
    
    def get_categories(self) -> list[str]:
        return self.categories
    
    def add_user(self, fighter: IFighter) -> None:
        self.user = fighter

class AttackAction(Action):
    categories = ["damage"]

    def __init__(self, user: Optional[IFighter] = None, damage: int = 0, on_self: bool = False, on_target: bool = False) -> None:
        super().__init__(user=user, on_self=on_self, on_target=on_target)
        self.damage = damage

    def execute(self, target: IFighter) -> bool:
        if not self.is_executable():
            return False
        if self.on_target:
            target.remove_hp(self.damage)
        if self.user and self.on_self:
            self.user.remove_hp(self.damage)
        return True

    def is_executable(self) -> bool:
        if self.user is None:
            return False
        return True

class HealAction(Action):
    categories = ["hp_regen"]

    def __init__(self, user: Optional[IFighter] = None, amount: int = 0, on_self: bool = False, on_target: bool = False):
        super().__init__(user, on_self=on_self, on_target=on_target)
        self.amount = amount

    def execute(self, target: IFighter) -> bool:
        if not self.is_executable():
            return False
        if self.on_target:
            target.add_hp(self.amount)
        if self.user and self.on_self:
            self.user.add_hp(self.amount)
        return True

    def is_executable(self) -> bool:
        if self.user is None:
            return False
        return True

class RegenerateMPAction(Action):
    categories = ["mp_regen"]
    
    def __init__(self, user: Optional[IFighter] = None, amount: int = 0, on_self: bool = False, on_target: bool = False):
        super().__init__(user=user, on_self=on_self, on_target=on_target)
        self.amount = amount

    def execute(self, target: IFighter) -> bool:
        if not self.is_executable():
            return False
        if self.on_target:
            target.add_mp(self.amount)
        if self.user and self.on_self:
            self.user.add_mp(self.amount)
        return True

    def is_executable(self) -> bool:
        if self.user is None:
            return False
        return True

class RegenerateStaminaAction(Action):
    categories = ["stamina_regen"]
    
    def __init__(self, user: Optional[IFighter] = None, amount: int = 0, on_self: bool = False, on_target: bool = False):
        super().__init__(user=user, on_self=on_self, on_target=on_target)
        self.amount = amount

    def execute(self, target: IFighter) -> bool:
        if not self.is_executable():
            return False
        if self.on_target:
            target.add_stamina(self.amount)
        if self.user and self.on_self:
            self.user.add_stamina(self.amount)
        return True

    def is_executable(self) -> bool:
        if self.user is None:
            return False
        return True

class LifeStealAction(Action):
    categories = ["damage", "hp_regen"]

    def __init__(self, user: Optional[IFighter] = None, damage: int = 0, heal: int = 0, damage_is_heal: bool = False, heal_multiplier: float = 1) -> None:
        super().__init__(user=user)
        self.damage = damage
        self.heal = heal

        if damage_is_heal:
            self.heal = round(damage * heal_multiplier)
    
    def execute(self, target: IFighter) -> bool:
        if not self.is_executable():
            return False
        target.remove_hp(self.damage)
        if self.user:
            self.user.add_hp(self.heal)
        return True

    def is_executable(self) -> bool:
        if self.user is None:
            return False
        return True
    
class ActionFactory():
    registry = {
        "attack": AttackAction,
        "heal": HealAction,
        "regen_mp": RegenerateMPAction,
        "regen_stamina": RegenerateStaminaAction,
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