# views/main_menu.py

import arcade
from constants import SCREEN_W, SCREEN_H, BG_COLOR
from views.gameplay import GameplayView
from views.settings import SettingsView

class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.bg_texture = arcade.load_texture("assets/bg_main.png")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.Color(*BG_COLOR))

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.bg_texture,
            arcade.XYWH(SCREEN_W // 2, SCREEN_H // 2, SCREEN_W, SCREEN_H)
        )
        
        # Title
        # arcade.draw_text("UNO", SCREEN_W / 2, SCREEN_H / 2 + 100,
        #                  arcade.color.RED, font_size=80, bold=True, anchor_x="center")
        # arcade.draw_text("ARCADE EDITION", SCREEN_W / 2, SCREEN_H / 2 + 40,
        #                  arcade.color.YELLOW, font_size=30, bold=True, anchor_x="center")

        # Instructions
        arcade.draw_text("Click anywhere to Start Game", SCREEN_W / 2, SCREEN_H / 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press 'S' for Settings", SCREEN_W / 2, SCREEN_H / 2 - 90,
                         arcade.color.LIGHT_GRAY, font_size=16, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameplayView()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.S:
            settings_view = SettingsView(self)
            self.window.show_view(settings_view)