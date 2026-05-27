from dependencies import*
from battle_entity.battle_entity import Hero
from arcade.gui import UIManager

class BattleUI:
    def __init__(self):
        self.manager = UIManager()
        self.manager.enable()
        
        # battle_event.on(EVENTS.BATTLE.PLAYER_TURN, self.on_player_turn)
        # battle_event.on(EVENTS.BATTLE.ENEMY_TURN, self.on_enemy_turn)
        # battle_event.on(EVENTS.UI.PREDICTION, self.on_prediction_update)

    def on_player_turn(self, hero: Hero):
        self.show_action_menu(hero)

    def on_prediction_update(self, turn_order):
        self.update_turn_order_display(turn_order)

    def draw(self):
        self.manager.draw()

    def cleanup(self):
        self.manager.disable()
        battle_event.off(EVENTS.UI.PLAYER_TURN, self.on_player_turn)
        battle_event.off(EVENTS.UI.PREDICTION, self.on_prediction_update)
        battle_event.off(EVENTS.UI.ENEMY_TURN, self.on_enemy_turn)