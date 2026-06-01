# views/settings.py

import arcade
from constants import SCREEN_W, SCREEN_H, BG_COLOR
# from main import main

class SettingsView(arcade.View):
    def __init__(self, previous_view):
        super().__init__()
        self.previous_view = previous_view
        self.mvol_c = arcade.color.YELLOW
        self.mus_c = arcade.color.LIGHT_GRAY
        self.sfx_c = arcade.color.LIGHT_GRAY
        self.pick_sett = 0


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
        arcade.draw_text(f"Master Volume:  [A]    {self.window.master_v}%   [D]", SCREEN_W / 2, SCREEN_H / 2 - 40,
                         self.mvol_c, font_size=20, anchor_x="center")
        arcade.draw_text(f"Music Volume:  [A]    {self.window.bgm_v}%   [D]", SCREEN_W / 2, SCREEN_H / 2 - 80,
                         self.mus_c, font_size=20, anchor_x="center")
        arcade.draw_text(f"Effect Volume:  [A]    {self.window.sfx_v}%   [D]", SCREEN_W / 2, SCREEN_H / 2 - 120,
                         self.sfx_c, font_size=20, anchor_x="center")
        arcade.draw_text("Press ESC to Return", SCREEN_W / 2, SCREEN_H / 2 - 160,
                         arcade.color.YELLOW, font_size=16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.previous_view)

        if key == arcade.key.S and self.pick_sett == 0:
            self.mus_c = arcade.color.YELLOW
            self.mvol_c = arcade.color.LIGHT_GRAY
            self.pick_sett = 1
        elif key == arcade.key.S and self.pick_sett == 1:
            self.sfx_c = arcade.color.YELLOW
            self.mus_c = arcade.color.LIGHT_GRAY
            self.pick_sett = 2
        elif key == arcade.key.S and self.pick_sett == 2:
            self.mvol_c = arcade.color.YELLOW
            self.sfx_c = arcade.color.LIGHT_GRAY
            self.pick_sett = 0

        if key == arcade.key.W and self.pick_sett == 0:
            self.sfx_c = arcade.color.YELLOW
            self.mvol_c = arcade.color.LIGHT_GRAY
            self.pick_sett = 2
        elif key == arcade.key.W and self.pick_sett == 1:
            self.mvol_c = arcade.color.YELLOW
            self.mus_c = arcade.color.LIGHT_GRAY
            self.pick_sett = 0
        elif key == arcade.key.W and self.pick_sett == 2:
            self.mus_c = arcade.color.YELLOW
            self.sfx_c = arcade.color.LIGHT_GRAY
            self.pick_sett = 1

        if key == arcade.key.A and self.pick_sett == 0 and self.window.master_v > 0:
            self.window.master_v -= 20
            self.window.master_vol = self.window.master_v / 100.0  # Instantly perfect math
            self._play_test_sfx()
            self._update_live_music()

        elif key == arcade.key.A and self.pick_sett == 1 and self.window.bgm_v > 0:
            self.window.bgm_v -= 20
            self.window.bgm_vol = self.window.bgm_v / 100.0
            self._update_live_music()

        elif key == arcade.key.A and self.pick_sett == 2 and self.window.sfx_v > 0:
            self.window.sfx_v -= 20
            self.window.sfx_vol = self.window.sfx_v / 100.0
            self._play_test_sfx()

            # --- D KEY (INCREASE) ---
        if key == arcade.key.D and self.pick_sett == 0 and self.window.master_v < 100:
            self.window.master_v += 20
            self.window.master_vol = self.window.master_v / 100.0
            self._play_test_sfx()
            self._update_live_music()

        elif key == arcade.key.D and self.pick_sett == 1 and self.window.bgm_v < 100:
            self.window.bgm_v += 20
            self.window.bgm_vol = self.window.bgm_v / 100.0
            self._update_live_music()

        elif key == arcade.key.D and self.pick_sett == 2 and self.window.sfx_v < 100:
            self.window.sfx_v += 20
            self.window.sfx_vol = self.window.sfx_v / 100.0
            self._play_test_sfx()

    def _play_test_sfx(self):
        """Plays a quick snap so the player hears the new SFX volume"""
        final_vol = self.window.sfx_vol * self.window.master_vol
        if final_vol > 0:
            test_sound = arcade.load_sound("assets/sfx/hover_deck.mp3")
            arcade.play_sound(test_sound, volume=final_vol)

    def _update_live_music(self):
        """Hunts down the active music track and turns the volume knob in real-time"""
        active_game = None
        if hasattr(self.previous_view, 'game_view'):
            active_game = self.previous_view.game_view

        # Check if we found the game AND if the track actually exists now
        if active_game and hasattr(active_game, 'music') and active_game.music:
            # Use 0.1 here to match the base_vol in gameplay.py!
            new_vol = 0.5 * self.window.bgm_vol * self.window.master_vol

            # Instantly change the track volume
            active_game.music.volume = new_vol