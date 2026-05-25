from __future__ import annotations
from ..dependencies import List, TYPE_CHECKING, ABC, copy
from ..battle_entity.entity_data import EntityData, HeroData, EnemyData
import arcade

if TYPE_CHECKING:
    from ..affect.affect import Affect, Offensive


class BattleEntity(arcade.Sprite, ABC):
    def __init__(self, data: EntityData, path_or_texture = None, scale = 1, center_x = 0, center_y = 0, angle = 0, **kwargs):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)

        self.data: EntityData = data
        self.data_predict: EntityData = None
        
        #anim instance things here from arcade

        self.is_selectable: bool = False
        self.update_predict()

        if type(self) is BattleEntity:
            raise TypeError(type(self).__name__, " is an Abstract class, cannot be instantiated")
        print(type(self).__name__, " Compiled successfully")
        
    def update_predict(self) -> None: #for now only need this
        self.data_predict = copy(self.data)
        self.data_predict.stat.luck = self.data.stat.luck
        self.data_predict.stat.speed = self.data.stat.speed
        

    def _reapply_affect(self) -> None:
        for affect in self.data.active_affects:
            if affect.is_tick and affect.duration > 0:
                affect.execute_affect([self])


    def tick_affects(self) -> None: # Duration: 2->trigger->1->trigger->0->delete
        self._reapply_affect()
        #anim_hurt
        if self.data.cur_hp <= 0:
            return
        
        expired: List[Affect] = []
        for affect in self.data.active_affects:
            affect.duration -= 1
            #add signal to ui here
            if affect.duration <= 0:
                expired.append(affect)
        
        for affect in expired:
            if not affect.is_tick and not isinstance(affect, Offensive):
                affect.revert_affect(self)
                #add signal to anim or vfx
            self.data.active_affects.remove(affect)
	
    def trigger_death_anim(self) -> None:
        pass
    
    def trigger_hurt_anim(self) -> None:
        pass
    
    def reset_after_battle(self) -> None:
        self.data.reset_stat()


class Hero(BattleEntity):
    def __init__(self, data: HeroData, path_or_texture=None, scale=1, center_x=0, center_y=0, angle=0, **kwargs):
        super().__init__(data, path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self.data: HeroData = data
    
    def reset_after_battle(self):
        if self.data.is_dead:
            return
        
        self.data.saved_hp = self.data.cur_hp
        self.data.saved_mp = self.data.cur_mp
        


class Enemy(BattleEntity):
    def __init__(self, data: EnemyData, path_or_texture=None, scale=1, center_x=0, center_y=0, angle=0, **kwargs):
        super().__init__(data, path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self.data: EnemyData = data


# Note
# When using the same data path for identical entities        

# DONT DO THIS, it references to the same data
dummy_data = HeroData()

tes_obj = Hero(data=dummy_data)
# tes_obj1 = Hero(data=dummy_data)
# tes_obj2 = Hero(data=dummy_data)

# DO THIS INSTEAD, make new instances of the same path
# dummy_data = HeroData()
# dummy_data1 = HeroData()
# dummy_data2 = HeroData()

# tes_obj = Hero(data=dummy_data)
# tes_obj1 = Hero(data=dummy_data1)
# tes_obj2 = Hero(data=dummy_data2)


# print(id(tes_obj.data.skill_list)) #omg it works 1!!1!!!1
# print(id(tes_obj1.data.skill_list)) #omg it works 1!!1!!!1
# print(id(tes_obj2.data.skill_list)) #omg it works 1!!1!!!1

print(tes_obj.data)


