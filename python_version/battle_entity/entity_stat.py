from __future__ import annotations
from dependencies import dataclass

@dataclass
class EntityStat:
    max_health: int = 9
    max_mana: int = 9
    strength: int = 9
    defense: int = 9
    speed: int = 9
    luck: int = 9

    level: int = 1
#Base Stats (Level 1)
    base_health: int = 1000
    base_mana: int = 100
    base_strength: int = 30 
    base_defense: int = 30
    base_speed: int = 100
    base_luck: int = 100

#Growth Rates
    health_growth: float = 1.1
    mana_growth: float = 1.05
    strength_growth: float = 1.08
    defense_growth: float = 1.08
    speed_growth: float = 1.03
    luck_growth: float = 1.03

    
    def _update_to_level(self) -> None:
        self.max_health   = int(self.base_health   * pow(self.health_growth,   self.level - 1))
        self.max_mana     = int(self.base_mana     * pow(self.mana_growth,     self.level - 1))
        self.strength = int(self.base_strength * pow(self.strength_growth, self.level - 1))
        self.defense  = int(self.base_defense  * pow(self.defense_growth,  self.level - 1))
        self.speed    = int(self.base_speed    * pow(self.speed_growth,    self.level - 1))
        self.luck     = int(self.base_luck     * pow(self.luck_growth,     self.level - 1))
    
    @classmethod
    def from_json(cls, data: dict) -> EntityStat:
        # 1. Filter out only the keys that exist as fields with annotation in our dataclass blueprint
        init_args = {k: v   for k, v in data.items() if k in cls.__annotations__ }
        # 2. make a class instance via @classmethod
        instance = cls(**init_args)
        # 3. update the stat for health, etc
        instance._update_to_level()
        # 4. get the instance
        return instance
    