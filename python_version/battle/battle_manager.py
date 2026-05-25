from ..dependencies import*
from ..battle_entity.battle_entity import BattleEntity, Hero, Enemy
from ..affect.affect import Affect

class _BattleManager:
    def __init__(self):
        self.state = BattleState.IDLE
        self.heroes: List[Hero]
        self.enemies: List[Enemy]
        self.exp_total: int
        self.all_entities: List[BattleEntity]
        self.alive_entities: List[BattleEntity]
        self.turn_order_cur: List[BattleEntity]
        self.turn_order_pred: List[BattleEntity]
        self.cur_entity: BattleEntity
        
    def state_change(self, new_state: BattleState):
        self.state = new_state

    def start_battle(self, heroes: List[Hero], enemies: List[Enemy]) -> None:
        self.heroes = heroes
        self.enemies = enemies
        
        for e in enemies:
            self.exp_total += e.data.exp_gain

        self.all_entities = heroes + enemies
        self.alive_entities = list(filter(lambda a: a.data.cur_hp > 0, self.all_entities))
        
        battle_event.emit(EVENTS.BATTLE.STARTED, heroes, enemies)

        battle_event.once(EVENTS.BATTLE.ANIMATION_FINISH, self._progress())

    
    def _progress(self) -> None:
        self.state_change(BattleState.PROGRESSING)


        
    def _get_cur_order(self, current_alive: List[BattleEntity]) -> List[BattleEntity]:

        pass

    def _update_order(self):
        self.turn_order_cur










BattleManager = _BattleManager() #load as singleton