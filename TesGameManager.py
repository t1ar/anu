from dependencies import*
from battle_entity.battle_entity import Hero, Enemy
from pyglet.window import Window
import arcade

    

class _GameManager(arcade.Window):
    def __init__(self):
        super().__init__(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            title="Project-square",
            update_rate=1/60,
            draw_rate=1/60,
            center_window=True,
            vsync=True,
        )
        self.main_menu = None
        self.battle_scene = None

    # def start_battle(self, Heroes: List[Hero], Enemies: List[Enemy]):
    #     from battle.battle_scene import BattleScene
    #     self.battle_scene = BattleScene(Heroes, Enemies, window=self)
    #     self.show_view(self.battle_scene)

#singleton
GameManager = _GameManager()

def main():
    from TESmain_menu import MainMenuView
    GameManager.main_menu = MainMenuView(window=GameManager)
    GameManager.show_view(GameManager.main_menu)
    arcade.run()

if __name__ == "__main__":
    main()











