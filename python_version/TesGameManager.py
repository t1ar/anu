from dependencies import*
from battle_entity.battle_entity import Hero, Enemy
from battle.battle_scene import BattleScene
from pyglet.window import Window
import arcade

class _GameManager(arcade.Window):
    def __init__(self):
        super().__init__(
            width=1280,
            height=720,
            title="Project-square",
            update_rate=1/60,
            draw_rate=1/60,
            center_window=True,
            vsync=True,
        )

    def start_battle(self, Heroes: List[Hero], Enemies: List[Enemy]):
        self.battle_scene = BattleScene(Heroes, Enemies)
        self.battle_scene.vie













#singleton
GameManager = _GameManager()