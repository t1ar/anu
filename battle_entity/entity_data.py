from __future__ import annotations
from dependencies import*
from battle_entity.entity_stat import EntityStat
from battle_entity.entity_cond import EntityCondition
import json

if TYPE_CHECKING:
    from ..affect.affect import Affect
    from ..battle_entity.skill import Skill


class TEAM(Enum):
    HERO = auto()
    ENEMY = auto()


@dataclass
class EntityData(ABC):
    name: str = "EntityName" #save on json
    team: TEAM = field(default=TEAM.HERO, init=False) #placeholder
    av: float = field(default=0.0, init=False) #placeholder

    cur_hp: int = field(default=0, init=False) #placeholder
    cur_mp: int = field(default=0, init=False) #placeholder

    eyeshot_path: str = "path_here" #save on json
    textures2_path: str = "path_here" #save on json
    textures3_path: str = "path_here" #save on json

    saved_stat: EntityStat = field(default_factory=EntityStat) #save on json
    stat: EntityStat = field(default_factory=EntityStat, init=False)

    skill_list_path: List[str] = field(default_factory=list) #save on json
    skill_list: List[Skill] = field(default_factory=list, init=False)

    active_affects: List[Affect] = field(default_factory=list, init=False)
    active_condition: EntityCondition = field(default_factory=EntityCondition, init=False)

    def __post_init__(self):
        if type(self) is EntityData:
            raise TypeError(type(self).__name__, " is an abstract class and cannot be instantiated")
        print(type(self).__name__, " Compiled successfully")
        self.reset_stat()
        
    def reset_stat(self) -> None:
        self.stat = copy(self.saved_stat)
        self.av = av_const / self.stat.speed

    def reset_av(self) -> float:
        self.av = av_const / self.stat.speed
        self.av += self.av * self.active_condition.delay
        self.av -= self.av * self.active_condition.advance
        self.av = max(self.av, 0.0)
        return self.av
    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> EntityData:
        ignored_keys = {"saved_stat"}
        init_args = {k: v for k, v in data.items() if k in cls.__annotations__ and k not in ignored_keys}

        loaded_saved_stat = EntityStat.from_json(data.get("saved_stat", {}))

        instance = cls(
            saved_stat=loaded_saved_stat,
            **init_args
        )

        # Unique isolated skill allocations
        instance.skill_list = []

        for path_str in instance.skill_list_path:
            file_path = Path(path_str)
            if file_path.exists():
                with open(file_path, "r") as file:
                    instance.skill_list.append(Skill.from_json(json.load(file)))

        return instance

#concrete class
@dataclass
class HeroData(EntityData):
    team: TEAM = field(init=False, default=TEAM.HERO)
    exp_to_lvl_up: int = field(init=False, default=100)
    cur_exp: int = 0 #save on json
    saved_hp: int = 0 #save on json
    saved_mp: int = 0 #save on json
    is_dead: bool = False #save on json
    is_init: bool = False #save on json

    def __post_init__(self):
        super().__post_init__()

        if not self.is_init:
            self.saved_hp = self.stat.max_health
            self.saved_mp = self.stat.max_mana
            self.is_init = True

        self.cur_hp = self.saved_hp
        self.cur_mp = self.saved_mp

        self.exp_to_lvl_up = 100 * pow(1.15, self.stat.level - 1)
    
    def add_exp(self, exp: int) -> None:
        self.cur_exp += exp
        if self.cur_exp >= self.exp_to_lvl_up:
            self.stat.level += 1
            self.cur_exp -= self.exp_to_lvl_up
            self.exp_to_lvl_up = 100 * pow(1.15, self.stat.level - 1)

    
    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> HeroData:
        instance: HeroData = super().from_json(data)
        instance.cur_exp = data.get("cur_exp", 0)
        instance.saved_hp = data.get("saved_hp", 0)
        instance.saved_mp = data.get("saved_mp", 0)
        instance.is_dead = data.get("is_dead", False)
        instance.is_init = data.get("is_init", False)

        return instance
    

@dataclass
class EnemyData(EntityData):
    team: TEAM = field(init=False, default=TEAM.ENEMY)
    exp_gain: int = 30 #save on json
    
    def __post_init__(self):
        super().__post_init__()

        self.cur_hp = self.stat.max_health
        self.cur_mp = self.stat.max_mana

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> EnemyData:
        instance: EnemyData = super().from_json(data)
        instance.exp_gain = data.get("exp_gain", 30)
        
        return instance
    

# tes_obj = HeroData() #debug if compiled correctly
# tes_obj = EnemyData() #debug if compiled correctly
# tes_obj = EntityData() #debug if compiled correctly