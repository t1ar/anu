# views/settings.py

import arcade
from constants import SCREEN_W, SCREEN_H, BG_COLOR

class SettingsView(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color.Color(*BG_COLOR))

    def on_draw(self):
        self.clear()
        
        # Dim overlay effect (though we just set background)
        arcade.draw_rect_filled(
            arcade.XYWH(SCREEN_W // 2, SCREEN_H // 2, SCREEN_W, SCREEN_H),
            arcade.color.Color(0, 0, 0, 150)
        )

        arcade.draw_text("SETTINGS MENU", SCREEN_W / 2, SCREEN_H / 2 + 100,
                         arcade.color.WHITE, font_size=40, bold=True, anchor_x="center")
        
        arcade.draw_text("Player Count: 3 (Fixed for now)", SCREEN_W / 2, SCREEN_H / 2,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Volume: 100%", SCREEN_W / 2, SCREEN_H / 2 - 40,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

        arcade.draw_text("Press ESC to Return", SCREEN_W / 2, SCREEN_H / 2 - 120,
                         arcade.color.YELLOW, font_size=16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)