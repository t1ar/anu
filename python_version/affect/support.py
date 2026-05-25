from __future__ import annotations
from ..dependencies import TYPE_CHECKING, dataclass, List
from ..affect.affect import Supportive

if TYPE_CHECKING:
    from ..affect.affect import BattleEntity

#DONT FORGET DEFAULT VALUE
@dataclass
class Support1(Supportive):
    pass




SUPPORT_MAP = {
    "Support1": Support1

}