from __future__ import annotations
from ..dependencies import*
from ..affect.affect import Affect, Offensive, Defensive, Supportive
from ..affect.defense import DEFENSE_MAP
from ..affect.support import SUPPORT_MAP
from ..affect.offense import OFFENSE_MAP

AFFECT_MAP = DEFENSE_MAP | SUPPORT_MAP | OFFENSE_MAP

@dataclass
class Skill:
    skill_name: str = "name here"
    # icon_path: str idk what to put here
    texture_path: str = "path_here"
    #bla bla bla all image, etc

    target_view: str = "SELF"

    element: str = "PHYSICAL" #ELEMENT : PHYSICAL | MAGIC
    success_rate: int = 100
    mp_cost: int = 15
    mp_regen: int = 0

    _offense: List[Offensive] = field(default_factory=list)
    _defense: List[Defensive] = field(default_factory=list)
    _support: List[Supportive] = field(default_factory=list)

    def __post_init__(self):
        print("Skill Compiled correctly")

    @property
    def affect_list(self) -> List[Affect]:
        return self._offense + self._defense + self._support

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Skill:
        #            init class~~v      for every subclass in dict~~~~~~~~~~v
        off_list = [AFFECT_MAP[name](**args) for name, args in data.get("offensive", {}).items() if name in AFFECT_MAP]
        def_list = [AFFECT_MAP[name](**args) for name, args in data.get("defensive", {}).items() if name in AFFECT_MAP]
        sup_list = [AFFECT_MAP[name](**args) for name, args in data.get("supportive", {}).items() if name in AFFECT_MAP]

        #init skill main data like name, texture_path etc
        init_args = {k: v for k, v in data.items() if k in cls.__annotations__}
        # for x, y in data.items() will give "keyword" as k, value as v. for every items in dict

        return cls(
            **init_args,
            _offense=off_list,
            _defense=def_list,
            _support=sup_list
        )
    

# tes_obj = Skill()