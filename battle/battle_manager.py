from dependencies import*
from battle_entity.battle_entity import BattleEntity, Hero, Enemy
from battle_entity.entity_data import TEAM
from affect.affect import Affect

#this is a singleton class, everyone can access the data freely
class _BattleManager:
    def __init__(self):
        self.state: BattleState = BattleState.IDLE
        self.heroes: List[Hero] = []
        self.enemies: List[Enemy] = []
        self.exp_total: int = 0
        self.all_entities: List[BattleEntity] = []
        self.alive_entities: List[BattleEntity] = []
        self.turn_order_cur: List[BattleEntity] = []
        self.turn_order_pred: List[BattleEntity] = []
        self.cur_entity: Optional[BattleEntity] = None
        
    def state_change(self, new_state: BattleState):
        self.state = new_state

    def start_battle(self, heroes: List[Hero], enemies: List[Enemy]) -> None:
        self.exp_total = 0
        self.heroes = heroes
        self.enemies = enemies
        
        for e in enemies:
            self.exp_total += e.data.exp_gain

        self.all_entities = heroes + enemies
        self.alive_entities = list(filter(lambda a: a.data.cur_hp > 0, self.all_entities))
        
        battle_event.on(EVENTS.ENTITY.DIED, self._on_entity_died)
        battle_event.on(EVENTS.ENTITY.ACTION, self._on_entity_action)

        battle_event.emit(EVENTS.BATTLE.START, heroes, enemies)
        battle_event.once(EVENTS.ANIMATION.FINISH, self._progress)

    def finish_battle(self):
        self.state_change(BattleState.ANIMATING)
        battle_event.off(EVENTS.ENTITY.DIED, self._on_entity_died)

    def _if_finished(self):
        if all(h.data.cur_hp <= 0 for h in self.heroes):
            battle_event.emit(EVENTS.BATTLE.FINISH_LOSE)

        if all(e.data.cur_hp <= 0 for e in self.enemies):
            battle_event.emit(EVENTS.BATTLE.FINISH_WIN)
        

    #event handler
    def _on_entity_died(self, entity: BattleEntity): #from Affect, affect knows if it killed an Entity
        self.state_change(BattleState.ANIMATING)
        self.alive_entities.remove(entity)
        self._update_all_order()
        entity.reset_after_battle()
        


    #update progress
    def _progress(self) -> None:
        self.state_change(BattleState.PROGRESSING) #UI/BattleScene reads tis

        if self._if_finished():
            self._finish_battle()
            return

        self._update_all_order()
        battle_event.emit(EVENTS.UI.PREDICTION, self.turn_order_pred)

        #debug
        for e in self.turn_order_pred:
            print("Prediction for next turn: ", e.data.name, " HERO" if e.data.team == TEAM.HERO else " ENEMY")

        self.cur_entity = self.turn_order_cur[0]

        self._update_view()

        self.cur_entity.tick_affects()

        if self.cur_entity not in self.alive_entities: #if entity died from tick affect
            self._update_progress() #reset progress, entity doesnt exist,
            return
        
        if self.cur_entity.data.active_condition.sleepy:
            self._update_progress() #reset progress, entity sleepy,
            return

        battle_event.once(EVENTS.ANIMATION.FINISH, self._update_progress)

    def _update_progress(self) -> None:
        self.state_change(BattleState.RESOLVING)
        for e in self.turn_order_cur:
            if e is self.cur_entity:
                continue
            e.data.av -= self.cur_entity.data.av
            e.update_predict()
        self.cur_entity.data.reset_av()
        self.cur_entity.update_predict()
        self._progress()

    def _on_entity_action(self, caster: BattleEntity, action: List[Affect], main_target: BattleEntity = None, 
                          mp_cost: int = 0, mp_regen: int = 0):
        caster.data.cur_mp += mp_regen - mp_cost
        caster.data.cur_mp = min(caster.data.cur_mp, caster.data.saved_stat.max_mana)
        caster.data.cur_mp = max(caster.data.cur_mp, 0)
        
        for a in action:
            targets = a.resolve_targets(caster, self.alive_entities)
            if not targets and main_target:
                targets = [main_target]
            a.apply_to(caster, targets)

    def _update_view(self): #WIP
        if isinstance(self.cur_entity, Hero):
            self.state_change(BattleState.PLAYER_TURN)
            battle_event.emit(EVENTS.BATTLE.PLAYER_TURN, self.cur_entity, self.alive_entities)
        elif isinstance(self.cur_entity, Enemy):
            self.state_change(BattleState.ENEMY_TURN)
            self.cur_entity.ai_pick(self.enemies, self.heroes)
            



    #turn order helper
    @staticmethod
    def _get_cur_order(current_alive: List[BattleEntity]) -> List[BattleEntity]:
        #negative = a comes first
        def comparator(a: BattleEntity, b: BattleEntity) -> int: 
            if a.data.av != b.data.av:
                return a.data.av - b.data.av 
            
            if a.data.stat.speed != b.data.stat.speed:
                return a.data.stat.speed - b.data.stat.speed

            if a.data.team != b.data.team:
                return -1 if a.data.team == TEAM.HERO else 1
            
            if a.data.stat.luck != b.data.stat.luck:
                return b.data.stat.luck - a.data.stat.luck
            
            return random.choice([-1, 1])
        
        return sorted(current_alive, key=cmp_to_key(comparator))

    @staticmethod #dict used for saving local data, so its not referenced 
    def _add_prediction_order(last_prediction: List[BattleEntity], av_sim: Dict[BattleEntity, float]):
        #negative = a comes first
        def comparator(a: BattleEntity, b: BattleEntity) -> int: 
            if av_sim[a] != av_sim[b]:
                return av_sim[a] - av_sim[b] 
            
            if a.data_predict.stat.speed != b.data_predict.stat.speed:
                return a.data_predict.stat.speed - b.data_predict.stat.speed

            if a.data.team != b.data.team:
                return -1 if a.data.team == TEAM.HERO else 1
            
            if a.data_predict.stat.luck != b.data_predict.stat.luck:
                return b.data_predict.stat.luck - a.data_predict.stat.luck
            
            return random.choice([-1, 1])
    
        entities = sorted(av_sim.keys(), key=cmp_to_key(comparator))

        lowest_av: float = av_sim[entities[0]]

        for e in entities:
            av_sim[e] -= lowest_av
        
        av_sim[entities[0]] = av_const / entities[0].data_predict.stat.speed

        last_prediction.append(entities[0])

    def _update_all_order(self):
        self.turn_order_cur = self._get_cur_order(self.alive_entities)

        av_sim: Dict[BattleEntity, float] = {}
        for e in self.turn_order_cur:
            av_sim[e] = e.data.av
        
        self.turn_order_pred = self.turn_order_cur.copy()
        while len(self.turn_order_pred) < 10:
            self._add_prediction_order(self.turn_order_pred, av_sim)

    










BattleManager = _BattleManager() #load as singleton