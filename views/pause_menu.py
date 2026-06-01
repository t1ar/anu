# views/pause_menu.py

import arcade
from constants import SCREEN_W, SCREEN_H
from views.settings import SettingsView

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gameplay import GameplayView

class PauseMenuView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view: GameplayView = game_view

    def on_draw(self):
        self.clear()
        # Draw the underlying game first
        self.game_view.on_draw()
        
        # Draw a semi-transparent screen over it
        arcade.draw_rect_filled(
            arcade.XYWH(SCREEN_W // 2, SCREEN_H // 2, SCREEN_W, SCREEN_H),
            arcade.color.Color(0, 0, 0, 200)
        )
        
        arcade.draw_text("PAUSED", SCREEN_W / 2, SCREEN_H / 2 + 50,
                         arcade.color.WHITE, font_size=50, bold=True, anchor_x="center")
        arcade.draw_text("Press ESC to Resume Game", SCREEN_W / 2, SCREEN_H / 2 - 20,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press 'S' for Settings", SCREEN_W / 2, SCREEN_H / 2 - 60,
                         arcade.color.LIGHT_GRAY, font_size=16, anchor_x="center")
        arcade.draw_text("Press 'R' to Restart", SCREEN_W / 2, SCREEN_H / 2 - 100,
                         arcade.color.YELLOW, font_size=16, anchor_x="center")
        arcade.draw_text("Press 'Q' to Quit to Menu", SCREEN_W / 2, SCREEN_H / 2 - 140,
                         arcade.color.RED, font_size=16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        elif key == arcade.key.S:
            settings_view = SettingsView(self)
            self.window.show_view(settings_view)
        elif key == arcade.key.Q:
            # Import here to avoid circular dependency
            from views.main_menu import MainMenuView
            menu_view = MainMenuView()
            self.window.show_view(menu_view)
            arcade.stop_sound(self.game_view.music_player)
        elif key == arcade.key.R:
            self.window.show_view(self.game_view)
            self.game_view._setup()