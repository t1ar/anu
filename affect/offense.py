from __future__ import annotations
from dependencies import TYPE_CHECKING, dataclass, List
from affect.affect import Offensive

if TYPE_CHECKING:
    from ..affect.affect import BattleEntity

#DONT FORGET DEFAULT VALUE
@dataclass
class Attack1(Offensive):
    target_type = "ALL_ENEMY"
    def execute_affect(self, targets):
        self.total_damage = 1
        for t in targets:
            t.data.cur_hp -= self.total_damage
            
        return super().execute_affect(targets)
    






OFFENSE_MAP = {
    "Attack1": Attack1
    
}