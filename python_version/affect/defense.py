from __future__ import annotations
from dependencies import TYPE_CHECKING, dataclass, List
from affect.affect import Defensive

if TYPE_CHECKING:
    from ..affect.affect import BattleEntity

#DONT FORGET DEFAULT VALUE
@dataclass
class AddDefense(Defensive):
    flat: int = 50
    scale: float = 1.0

    added: int = 0 # for reverting
    # multipler: float from self.caster

    def execute_affect(self, targets: List[BattleEntity]):
        for t in targets:
            self.added = self.flat * self.scale * self.caster.data.stat.defense_growth
            t.data.stat.defense += self.added
            
        
    def revert_affect(self, target: BattleEntity):
        target.data.stat.defense -= self.added
        
#other concrete class here






DEFENSE_MAP = {
    "AddDefense": AddDefense

}