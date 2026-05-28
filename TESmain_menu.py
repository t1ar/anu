from dependencies import*
import arcade




class MainMenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text("MAIN MENU", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("Press ENTER to play", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            from TESview import FieldView
            loading = LoadingView(next_view=FieldView())
            self.window.show_view(loading)


class LoadingView(arcade.View):
    def __init__(self, next_view: arcade.View):
        super().__init__()
        self.next_view = next_view
        self.progress = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_update(self, delta_time):
        self.progress += delta_time * 150  # simulate loading
        if self.progress >= 100:
            self.window.show_view(self.next_view)

    def on_draw(self):
        self.clear()
        arcade.draw_text(f"Loading... {int(self.progress)}%",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=24, anchor_x="center")

