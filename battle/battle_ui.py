from dependencies import*
from battle_entity.battle_entity import Hero, Enemy, BattleEntity
from battle.battle_manager import BattleManager
import arcade.gui

class BattleUI:
    def __init__(self, heroes: List[Hero], enemies: List[Enemy]):
        self.anchor_skill = None #skill
        self.action_layout = None

        self.heroes = heroes
        self.enemies = enemies
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.setup()

        battle_event.on(EVENTS.ENTITY.HURT, self._on_entity_hurt)
        battle_event.on(EVENTS.BATTLE.PLAYER_TURN, self._on_player_turn)
        battle_event.on(EVENTS.ENTITY.ACTION, self._on_entity_action)
        battle_event.on(EVENTS.UI.PREDICTION, self._on_prediction_update)

    def setup(self):
        self.hp_labels = {}  # entity -> UILabel
        self.button = arcade.gui.UIFlatButton(text="Click Me", width=200, height=50)

        for hero in self.heroes:
            label_hero = arcade.gui.UILabel(
                text=f"{hero.data.name} HP: {hero.data.cur_hp}",
                width=80,
                height=25,
                text_color=arcade.color.WHITE
            )

            anchor_hero = arcade.gui.UIAnchorLayout()
            anchor_hero.add(
                child=label_hero,
                anchor_x="center_x",
                anchor_y="bottom",
                align_y=80         # above the action buttons
            )
            
            self.manager.add(anchor_hero)
            self.hp_labels[hero] = label_hero

        for enemy in self.enemies:
            label_enemy = arcade.gui.UILabel(
                text=f"{enemy.data.name} HP: {enemy.data.cur_hp}",
                width=80,
                height=25,
                text_color=arcade.color.WHITE
            )

            anchor_enemy = arcade.gui.UIAnchorLayout()
            anchor_enemy.add(
                child=label_enemy,
                anchor_x="center_x",
                anchor_y="top",
                align_y=-20        # padding from top
            )
            self.manager.add(anchor_enemy)
            self.hp_labels[enemy] = label_enemy
        
         # action buttons
        
        # self.attack_btn = arcade.gui.UIFlatButton(text="Attack", width=120, height=40)
        # self.skill_btn = arcade.gui.UIFlatButton(text="Skill", width=120, height=40)
        # self.flee_btn = arcade.gui.UIFlatButton(text="Flee", width=120, height=40)

        # @self.attack_btn.event("on_click")
        # def on_attack(event):
        #     pass
        #     # battle_event.emit(EVENTS.BATTLE.PLAYER_ACTION, action="attack")

        # @self.skill_btn.event("on_click")
        # def on_skill(event):
        #     pass
        #     # battle_event.emit(EVENTS.BATTLE.PLAYER_ACTION, action="skill")

        # @self.flee_btn.event("on_click")
        # def on_flee(event):
        #     pass
        #     # battle_event.emit(EVENTS.BATTLE.PLAYER_ACTION, action="flee")

        # # group buttons in a layout
        # self.action_layout = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        # self.action_layout.add(self.attack_btn)
        # self.action_layout.add(self.skill_btn)
        # self.action_layout.add(self.flee_btn)

        # place at bottom center
        # anchor = arcade.gui.UIAnchorLayout()
        # anchor.add(
        #     child=self.action_layout,
        #     anchor_x="center_x",
        #     anchor_y="bottom",
        #     align_y=20   # padding from bottom
        # )
        # self.manager.add(anchor)

        # # hide by default
        # self.action_layout.visible = False

    def draw(self):
        self.manager.draw()
        

    def cleanup(self):
        self.manager.disable()
        battle_event.off(EVENTS.BATTLE.PLAYER_TURN, self._on_player_turn)
        battle_event.off(EVENTS.BATTLE.ENEMY_TURN, self._on_enemy_turn)
        battle_event.off(EVENTS.UI.PREDICTION, self._on_prediction_update)

    def _clear_action_buttons(self):
        if self.anchor_skill:
            self.manager.remove(self.anchor_skill)
            self.anchor_skill = None
            self.action_layout = None

    def _on_entity_died(self, entity: BattleEntity):
        print("died")
        self.hp_labels[entity].text = f"DIED, HP: 0"


    def _on_entity_hurt(self, entity: BattleEntity):
        print(entity.data.name, "got targeted")

        def update_hp(*args):
            print(entity.data.name, "got hurted")
            self.hp_labels[entity].text = f"{entity.data.name} HP: {entity.data.cur_hp}"
    
        battle_event.once(EVENTS.ANIMATION.FINISH, update_hp)



    def _on_player_turn(self, hero: Hero):
        # print("UI received player turn", hero.data.name)
        # print("Total skills:", hero.data.skill_list)
        if BattleManager.state != BattleState.PLAYER_TURN:
            print("guarded player spam")
            return
        
        self._clear_action_buttons()  # remove old buttons first

        self.action_layout = arcade.gui.UIBoxLayout(vertical=False, space_between=10)

        # build a button for each skill the hero has
        for skill in hero.data.skill_list:
            btn = arcade.gui.UIFlatButton(text=skill.skill_name, width=120, height=40)

            @btn.event("on_click")
            def on_click(event, s=skill):
                #para = caster, affects, main_target, mp_cost, mp_regen
                battle_event.emit(EVENTS.ENTITY.ACTION, hero, s.affect_list)
                


            self.action_layout.add(btn)

        # print("total buttons:", len(self.action_layout.children))

        self.anchor_skill = arcade.gui.UIAnchorLayout()
        self.anchor_skill.add(
            child=self.action_layout,
            anchor_x="center_x",
            anchor_y="bottom",
            align_y=20
        )
        self.manager.add(self.anchor_skill)
        

    def _on_entity_action(self, *args):
        print("cleared button")
        self._clear_action_buttons()

    def _on_prediction_update(self, turn_order):
        # self.update_turn_order_display(turn_order)
        pass