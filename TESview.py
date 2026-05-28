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
    if key == arcade.key.ENTER:
        # placeholder — replace with real hero/enemy data later
        tes_data1 = HeroData()
        tes_data2 = EnemyData()
        heroes = [Hero(tes_data1)]
        enemies = [Enemy(tes_data2)]

        self.window.start_battle(heroes, enemies)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.B:
            battle = BattleView(return_view=self)
            self.window.show_view(battle)
        elif key == arcade.key.ESCAPE:
            self.window.show_view(MainMenuView())


class BattleView(arcade.View):
    def __init__(self, return_view: arcade.View):
        super().__init__()
        self.return_view = return_view  # go back to field after battle

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_RED)

    def on_draw(self):
        self.clear()
        arcade.draw_text("BATTLE SCENE", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=36, anchor_x="center")
        arcade.draw_text("Press ESC to flee", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.LIGHT_GRAY, font_size=18, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.return_view)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "My Game")
        self.show_view(MainMenuView())


def main():
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()