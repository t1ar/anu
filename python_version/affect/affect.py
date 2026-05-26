from __future__ import annotations
from dependencies import TYPE_CHECKING, dataclass, field, ABC, abstractmethod, copy, List, battle_event, EVENTS

if TYPE_CHECKING:
    from battle_entity.battle_entity import BattleEntity


# Target Blueprint Guide :
# "SELF", "SINGLE_ALLY", "ALL_ALLIES", "SINGLE_ENEMY", "ALL_ENEMY"

# Base Interface
@dataclass
class Affect(ABC):
    caster: BattleEntity = field(init=False, default=None)
    target_type: str = "SELF" #used on .json
    duration: int = 0 #0 = one-time instances #used on .json
    is_tick: bool = False #used on .json

    #concrete method
    def apply_to(self, caster_: BattleEntity, targets: List[BattleEntity]) -> None:
        if not targets:
            return
        for t in targets:
            dupe: Affect = copy(self)
            dupe.caster = caster_
            t.data.active_affects.append(dupe)
            if not self.is_tick:
                dupe.execute_affect([t])

    def resolve_targets(self, caster: BattleEntity, all_entities: List[BattleEntity]) -> List[BattleEntity]: 
        allies :List[BattleEntity] = [e for e in all_entities if e.data.team == caster.data.team]
        enemies: List[BattleEntity] = [e for e in all_entities if e.data.team != caster.data.team]

        match self.target_type:
            case "SELF":
                return [caster]
            case "SINGLE_ALLY":
                return []
            case "ALL_ALLIES":
                return allies
            case "SINGLE_ENEMY":
                return []
            case "ALL_ENEMY":
                return enemies
            case _: #default case, if no match
                return []

    @abstractmethod #used by all
    def execute_affect(self, targets: List[BattleEntity]) -> None: pass

    @abstractmethod #used for offensive & support only
    def predict_affect(self, caster: BattleEntity, targets: List[BattleEntity]) -> None:pass
    
    @abstractmethod #used by defensive & support only
    def revert_affect(self, target: BattleEntity) -> None: pass


# Intermediate Categories
@dataclass
class Offensive(Affect, ABC):
    #used by offensive's child as super() at the end of func
    total_damage = field(default=0, init=False)

    def execute_affect(self, targets) -> None:
        for t in targets:
            battle_event.emit(EVENTS.UI.DAMAGE, self.total_damage, self.caster, t)

            if t.data.cur_hp <= 0:
                battle_event.emit(EVENTS.ENTITY.DIED, t) #BattleScene will read
            else:
                battle_event.emit(EVENTS.ENTITY.HURT, t) #BattleScene will read
    
    #skip usage
    def revert_affect(self, target: BattleEntity):
        pass

    
@dataclass
class Defensive(Affect, ABC):
    #skip usage
    def predict_affect(self, caster: BattleEntity, targets: List[BattleEntity]):
        pass
    pass

@dataclass
class Supportive(Affect, ABC):
    pass