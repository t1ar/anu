from dependencies import*
from battle_entity.battle_entity import Hero, Enemy, HeroData, EnemyData
import arcade

    

class MainMenuScene(arcade.View):
    def __init__(self, window = None, background_color = None):
        super().__init__(window, background_color)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Press ENTER to start", 640, 360, arcade.color.WHITE, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            # placeholder — replace with real hero/enemy data later
            tes_data1 = HeroData()
            tes_data2 = EnemyData()
            heroes = [Hero(tes_data1)]
            enemies = [Enemy(tes_data2)]
            from TesGameManager import GameManager
            self.window
            GameManager.start_battle(heroes, enemies)