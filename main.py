# main.py

import arcade
from constants import SCREEN_W, SCREEN_H, TITLE
from views.main_menu import MainMenuView

def main():
    arcade.load_font("assets/fonts/DMSans.ttf")
    window = arcade.Window(SCREEN_W, SCREEN_H, TITLE, resizable=False, antialiasing=8)

    window.sfx_vol = 1.0  # Controls only sound effects
    window.master_vol = 1.0  # Controls everything
    window.bgm_vol = 1.0  # Controls only background music
    window.master_v = 100 # master volume gui in setting
    window.bgm_v = 100 # background music gui in setting
    window.sfx_v = 100 # sound effect gui in setting

    # Initialize the starting view
    menu_view = MainMenuView()
    window.show_view(menu_view)
    
    # Run the engine
    arcade.run()

if __name__ == "__main__":
    from models import preload_card
    preload_card()

    main()