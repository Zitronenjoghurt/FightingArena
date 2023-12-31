from ..interfaces.fighter_protocol import IFighter

class Effect():
    name = ""
    categories = []
    message = ""

    DISALLOW_ATTACK_EFFECTS = ["frozen"]

    def __init__(self, duration: int = 0, on_self: bool = False, on_target: bool = False) -> None:
        self.duration = duration
        self.on_self = on_self
        self.on_target = on_target
    
    def execute(self, target: IFighter) -> str:
        return ""
    
    def on_apply(self, target: IFighter) -> None:
        pass
    
    def on_remove(self, target: IFighter) -> None:
        pass

    def apply_on_self(self) -> bool:
        return self.on_self
    
    def apply_on_target(self) -> bool:
        return self.on_target

    def get_duration(self) -> int:
        return self.duration
    
    def get_categories(self) -> list[str]:
        return self.categories
    
    def get_name(self) -> str:
        return self.name

class BurnEffect(Effect):
    name = "burning"
    categories = ["burn"]
    message = "{target} is burning, -{damage}HP"

    def __init__(self, duration: int = 0, damage: int = 0, on_self: bool = False, on_target: bool = False) -> None:
        super().__init__(duration=duration, on_self=on_self, on_target=on_target)
        self.damage = damage

    def execute(self, target: IFighter) -> str:
        target.remove_hp(self.damage)
        return self.message.format(target=target.get_name(), damage=self.damage)
    
class FreezeEffect(Effect):
    name = "frozen"
    categories = ["freeze"]
    message = "{target} is frozen and unable to attack."

    def execute(self, target: IFighter) -> str:
        if not target.has_attacked():
            return self.message.format(target=target.get_name())
        return ""
    
    def on_apply(self, target: IFighter) -> None:
        target.disallow_attack()
    
    def on_remove(self, target: IFighter) -> None:
        if not target.has_effects(self.DISALLOW_ATTACK_EFFECTS):
            target.allow_attack()

class EffectFactory():
    registry = {
        "burn": BurnEffect,
        "freeze": FreezeEffect
    }

    @staticmethod
    def create_effect(effect_type: str, effect_args: dict) -> Effect:
        EffectClass = EffectFactory.registry.get(effect_type, None)

        if EffectClass is None:
            raise ValueError(f"Effect type {effect_type} not found")
        try:
            effect = EffectClass(**effect_args)
        except TypeError:
            raise ValueError(f"Invalid arguments for effect type {effect_type}")
        
        return effect