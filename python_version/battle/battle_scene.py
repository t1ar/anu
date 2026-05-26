from dependencies import*
from battle_entity.battle_entity import Hero, Enemy
from battle.battle_ui import BattleUI
from battle.battle_manager import BattleManager
import arcade

class BattleScene(arcade.View):
    def __init__(self, Heros: List[Hero], Enemies: List[Enemy], window = None, background_color = None,):
        super().__init__(window, background_color)
        self.ui = BattleUI()
        BattleManager.start_battle(Heros, Enemies)

    def on_draw(self):
        self.clear()
        self.ui.draw()

    def on_hide_view(self):
        self.ui.cleanup()
        BattleManager.finish_battle()