# main.py

import arcade
from constants import SCREEN_W, SCREEN_H, TITLE
from views.main_menu import MainMenuView

def main():
    window = arcade.Window(SCREEN_W, SCREEN_H, TITLE, resizable=False)
    
    # Initialize the starting view
    menu_view = MainMenuView()
    window.show_view(menu_view)
    
    # Run the engine
    arcade.run()

if __name__ == "__main__":
    main()