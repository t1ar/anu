from dependencies import*
from battle_entity.battle_entity import Hero, Enemy
from battle_entity.entity_data import HeroData, EnemyData
import arcade


class FieldView(arcade.View):
    def __init__(self):
        super().__init__()
        # arcade.Scene is used HERE — to organize sprites within this view
        self.scene = arcade.Scene()
        self.player = arcade.SpriteSolidColor(32, 32, arcade.color.YELLOW)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = SCREEN_HEIGHT / 2
        self.scene.add_sprite("player", self.player)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        arcade.draw_text("FIELD  |  Press B to battle",
                         10, 10, arcade.color.WHITE, font_size=14)

    def on_update(self, delta_time):
        self.scene.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.B:
            from battle.battle_scene import BattleScene
            tes_data1 = HeroData(name="Cirno")
            tes_data2 = EnemyData(name="Evil cirno")
            heroes = [Hero(tes_data1)]
            enemies = [Enemy(tes_data2)]
            battle = BattleScene(self, heroes, enemies)
            self.window.show_view(battle)
        elif key == arcade.key.ESCAPE:
            from TESmain_menu import MainMenuView
            self.window.show_view(MainMenuView())

