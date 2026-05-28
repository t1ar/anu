from dependencies import*
from battle_entity.battle_entity import BattleEntity, Hero, Enemy
from battle.battle_manager import BattleManager
from battle.battle_ui import BattleUI
import arcade

class BattleScene(arcade.View):
    def __init__(self, Heros: List[Hero], Enemies: List[Enemy], window = None, background_color = None,):
        super().__init__(window, background_color)
        self.ui = BattleUI()
        BattleManager.start_battle(Heros, Enemies)
        battle_event.on(EVENTS.ENTITY.HURT, self._on_entity_hurt)
        battle_event.on(EVENTS.ENTITY.DIED, self._on_entity_died)

    def on_draw(self):
        self.clear()
        self.ui.draw()
        arcade.draw_text("Battle Scene Active", 640, 360, arcade.color.RED, anchor_x="center")

    def on_hide_view(self):
        self.ui.cleanup()
    
    def _on_entity_hurt(self, entity: BattleEntity):
        entity.trigger_hurt_anim()

    def _on_entity_died(self, entity: BattleEntity):
        entity.trigger_death_anim()