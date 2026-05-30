# main.py

import arcade
from constants import SCREEN_W, SCREEN_H, TITLE
from views.main_menu import MainMenuView

def main():
    arcade.load_font("assets/fonts/NotoEmoji.ttf")
    arcade.load_font("assets/fonts/NotoColorEmoji.ttf")
    arcade.load_font("assets/fonts/DMSans.ttf")
    arcade.load_font("assets/fonts/DMSansItalic.ttf")
    window = arcade.Window(SCREEN_W, SCREEN_H, TITLE, resizable=False)
    
    # Initialize the starting view
    menu_view = MainMenuView()
    window.show_view(menu_view)
    
    # Run the engine
    arcade.run()

if __name__ == "__main__":
    main()