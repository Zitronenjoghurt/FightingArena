from ..interfaces.fighter_protocol import IFighter

class Effect():
    name = ""
    categories = []
    message = ""
    
    def execute(self, target: IFighter) -> str:
        return ""

    def get_duration(self) -> int:
        return self.duration
    
    def get_categories(self) -> list[str]:
        return self.categories
    
    def get_name(self) -> str:
        return self.name

class BurnEffect(Effect):
    name = "burn"
    categories = ["burn"]
    message = "{target} is burning, -{damage}HP"

    def __init__(self, duration: int, damage: int) -> None:
        self.duration = duration
        self.damage = damage

    def execute(self, target: IFighter) -> str:
        target.remove_hp(self.damage)
        return self.message.format(target=target.get_name(), damage=self.damage)

class EffectFactory():
    registry = {
        "burn": BurnEffect
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