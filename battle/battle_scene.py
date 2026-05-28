from dependencies import*
from battle_entity.battle_entity import BattleEntity, Hero, Enemy
from battle.battle_manager import BattleManager
from battle.battle_ui import BattleUI
import arcade

class BattleScene(arcade.View):
    def __init__(self, return_view: arcade.View, Heros: List[Hero], Enemies: List[Enemy]):
        super().__init__()
        self.return_view = return_view
        self.ui = BattleUI(Heros, Enemies)
        self.all_sprites = arcade.SpriteList()

        self.Heroes = Heros
        self.Enemies = Enemies
        BattleManager.start_battle(Heros, Enemies)
        battle_event.on(EVENTS.ANIMATION.START, self._on_trigger_animation)
        battle_event.on(EVENTS.ENTITY.HURT, self._on_entity_hurt)
        battle_event.on(EVENTS.ENTITY.DIED, self._on_entity_died)

        for e in self.Heroes:
            e.center_x = 240
            e.center_y = 100
            self.all_sprites.append(e)

        for e in self.Enemies:
            e.center_x = 240
            e.center_y = 560
            self.all_sprites.append(e)
        


    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self):
        self.clear()
        # arcade.draw_text("BATTLE SCENE", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                     arcade.color.WHITE, font_size=36, anchor_x="center")
        # arcade.draw_text("Press ESC to flee", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
        #                     arcade.color.LIGHT_GRAY, font_size=18, anchor_x="center")
        self.all_sprites.draw()
        self.ui.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.return_view)

    def on_hide_view(self):
        self.ui.cleanup()
    
    @staticmethod
    def wait_anim(duration, entity_name):
        def finish(dt):
            print("anim_finished", entity_name)
            battle_event.emit(EVENTS.ANIMATION.FINISH)
        arcade.schedule_once(finish, duration)

    def _on_trigger_animation(self, entity: BattleEntity): #animation simulation 
        self.wait_anim(0.5, entity.data.name)

    def _on_entity_hurt(self, entity: BattleEntity):
        entity.trigger_hurt_anim()

    def _on_entity_died(self, entity: BattleEntity):
        entity.trigger_death_anim()