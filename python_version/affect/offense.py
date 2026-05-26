from __future__ import annotations
from dependencies import TYPE_CHECKING, dataclass, List
from affect.affect import Offensive

if TYPE_CHECKING:
    from ..affect.affect import BattleEntity

#DONT FORGET DEFAULT VALUE
@dataclass
class Attack1(Offensive):
    pass




OFFENSE_MAP = {
    "Attack1": Attack1
    
}