from ..dependencies import dataclass

@dataclass
class EntityCondition:
    advance: float = 0.0
    delay: float = 0.0
    shield_hp: int = 0
    damage_reduction: float = 0.0 #range 0 -> 0.9
    sleepy: bool = False #skip turn when self.action
    exhausted: bool = False #cant use skill that consume mp
    unseen: bool = False #cant be single-targeted
    