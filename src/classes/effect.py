from ..interfaces.fighter_protocol import IFighter

class Effect():
    def execute(self, target: IFighter) -> None:
        pass

    def get_duration(self) -> int:
        return self.duration

class BurnEffect(Effect):
    def __init__(self, duration: int, damage: int) -> None:
        self.duration = duration
        self.damage = damage

    def execute(self, target: IFighter) -> None:
        target.remove_hp(self.damage)

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