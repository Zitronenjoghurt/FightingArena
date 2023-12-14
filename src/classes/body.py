from typing import Optional
from ..interfaces.fighter_protocol import IFighter

class BodyPart():
    def __init__(self, name: str, inside_of: Optional[str] = None) -> None:
        self.name = name
        self.inside_of = inside_of

class Body():
    def __init__(self, fighter: Optional[IFighter] = None, body_parts: Optional[list[BodyPart]] = None) -> None:
        self.fighter = fighter
        self.body_parts = body_parts

    @staticmethod
    def create(body_parts_list: list[dict]) -> 'Body':
        body_parts = []
        for body_part_data in body_parts_list:
            body_part = BodyPartFactory.create_body_part(body_part_data)
            body_parts.append(body_part)
        return Body(body_parts=body_parts)
    
    def add_fighter(self, fighter: IFighter) -> None:
        self.fighter = fighter

class ExtremityPart(BodyPart):
    pass

class HeadPart(BodyPart):
    pass

class VitalPart(BodyPart):
    pass

class BodyPartFactory():
    registry = {
        "extremity": ExtremityPart,
        "head": HeadPart,
        "vital": VitalPart
    }

    @staticmethod
    def create_body_part(part_data: dict) -> BodyPart:
        part_type = part_data.get("type", None)
        if not part_type:
            ValueError(f"Unable to retrieve type for given body part\n{part_data}")

        BodyPartClass = BodyPartFactory.registry.get(part_type, None)

        if BodyPartClass is None:
            raise ValueError(f"Body part type {part_type} not found")
        try:
            body_part = BodyPartClass(**part_data)
        except TypeError:
            raise ValueError(f"Invalid arguments for body part type {part_type}")
        
        return body_part