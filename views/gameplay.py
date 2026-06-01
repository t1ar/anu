# views/gameplay.py

import arcade
import math
import random
from typing import Optional

from constants import *
from models import Card, Player, build_deck, draw_card, _card_label
from views.pause_menu import PauseMenuView

# States specific only to the active game
STATE_PLAYER_TURN   = "player_turn"
STATE_CPU_THINKING  = "cpu_thinking"
STATE_PICK_COLOR    = "pick_color"
STATE_GAME_OVER     = "game_over"
STATE_DEALING       = "dealing"

class GameplayView(arcade.View):
    def __init__(self):
        super().__init__()
        self._setup()

    def _setup(self):
        self.deck: list[Card] = build_deck()
        self.discard: list[Card] = []

        self.bg_texture = arcade.load_texture("assets/bg_gameplay.png")
        self.arrow_cw_texture = arcade.load_texture("assets/arrow.png")
        self.arrow_ccw_texture = self.arrow_cw_texture.flip_horizontally()

        self.sound_start = arcade.load_sound("assets/sfx/shuffle_deck.mp3")
        self.sound_play = arcade.load_sound("assets/sfx/play_card.mp3")
        self.sound_draw = arcade.load_sound("assets/sfx/take_card.mp3")
        self.sound_hover = arcade.load_sound("assets/sfx/hover_deck.mp3")

        self.bg_arrow_angle = 0.0

        self.total_time = 0.0

        possible_names = []
        try:
            with open("assets/bot_names.txt", "r") as file:
                # Read all lines, strip the hidden \n from the end of each, and ignore blank lines
                for line in file:
                    clean_name = line.strip()
                    if clean_name:
                        possible_names.append(clean_name)

        except FileNotFoundError:
            print("Warning: assets/bot_names.txt missing! Using default bot names.")
            # The ultimate safety net fallback
            possible_names = ["Bot A", "Bot B", "Bot C", "Bot D"]

        chosen_names = random.sample(possible_names, 3)

        self.players = []
        self.players.append(Player("You", is_human=True))

        for i in range(3):
            self.players.append(Player(chosen_names[i], is_human=False))

        self.current_idx = 0
        self.direction = 1          
        self.state = STATE_DEALING
        self.deal_timer = 0.0
        self.cpu_timer = 0.0
        self.message = ""
        self.message_timer = 0.0
        self.winner: Optional[Player] = None
        self.hover_idx: Optional[int] = None
        self.selected_idx: Optional[int] = None    
        self.drew_this_turn = False                

        # Deal cards
        for _ in range(DEAL_CARDS):
            for p in self.players:
                if self.deck:
                    p.hand.append(self.deck.pop())

        # First discard — skip wilds
        while True:
            card = self.deck.pop()
            if not card.is_wild:
                self.discard.append(card)
                break
            self.deck.insert(0, card)

        self.state = STATE_PLAYER_TURN
        self.play_sfx(self.sound_start)

        # 1. If music is already playing from a previous game, stop it first!
        if hasattr(self, 'music_player') and self.music_player is not None:
            arcade.stop_sound(self.music_player)

        # 2. Load the track
        self.bg_music = arcade.load_sound("assets/bgm/anu_bgm.mp3")

        # 3. Play it and save the player reference
        self.music_player = arcade.play_sound(self.bg_music, volume=0.1, loop=True)



    @property
    def current_player(self) -> Player:
        return self.players[self.current_idx]

    @property
    def top_card(self) -> Card:
        return self.discard[-1]

    def on_show_view(self):
        arcade.set_background_color(arcade.color.Color(*BG_COLOR))

    def on_update(self, delta_time: float):

        spin_speed = 30
        self.total_time += delta_time

        if self.direction == 1:
            self.bg_arrow_angle += spin_speed * delta_time
        else:
            self.bg_arrow_angle -= spin_speed * delta_time

        if self.message_timer > 0:
            self.message_timer -= delta_time

        if self.state == STATE_CPU_THINKING:
            self.cpu_timer -= delta_time
            if self.cpu_timer <= 0:
                self._cpu_play()

            # --- NEW ANIMATION LOGIC ---
            # Constantly check if targets need to shift (like when hovering)
        if self.state == STATE_PLAYER_TURN:
            self.update_card_targets()

            # Update physical positions of all cards in play
        for player in self.players:
            for card in player.hand:
                card.update()
        for card in self.discard:
            card.update()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.bg_texture,
            arcade.XYWH(SCREEN_W // 2, SCREEN_H // 2, SCREEN_W, SCREEN_H)
        )

        current_arrow = self.arrow_cw_texture if self.direction == 1 else self.arrow_ccw_texture

        w = current_arrow.width
        h = current_arrow.height

        arrow_size = 500
        arcade.draw_texture_rect(
            current_arrow,
            arcade.XYWH(SCREEN_W // 2, SCREEN_H // 2, w, h),
            angle=self.bg_arrow_angle
        )

        self._draw_discard()
        self._draw_deck_pile()
        self._draw_cpu_hands()
        self._draw_player_hand()
        self._draw_hud()
        if self.state == STATE_PICK_COLOR:
            self._draw_color_picker()
        if self.state == STATE_GAME_OVER:
            self._draw_game_over()

    def update_card_targets(self):
        """Calculates where every card SHOULD be and updates their targets."""

        # 1. Update Human Player targets (Bottom)
        player = self.players[0]
        n = len(player.hand)
        if n > 0:
            spread = min(n * (CARD_W + 6), SCREEN_W - 160)
            start_x = SCREEN_W // 2 - spread // 2 + CARD_W // 2

            for i, card in enumerate(player.hand):
                card.target_x = start_x + i * (spread // max(n - 1, 1)) if n > 1 else SCREEN_W // 2

                # Lift the card if it's playable or hovered
                is_my_turn = (self.current_idx == 0 and self.state == STATE_PLAYER_TURN)
                playable = card.can_play_on(self.top_card) if is_my_turn else False
                hover = (self.hover_idx == i) and is_my_turn

                lift = 20 if hover else (8 if playable and is_my_turn else 0)
                card.target_y = 70 + lift

        # 2. Update CPU targets
        positions = [
            (80, SCREEN_H // 2),  # Left Bot
            (SCREEN_W // 2, SCREEN_H - 80),  # Top Bot
            (SCREEN_W - 80, SCREEN_H // 2),  # Right Bot
        ]

        for idx, cpu in enumerate(self.players[1:], 1):
            if idx - 1 >= len(positions):
                break

            px, py = positions[idx - 1]
            n = len(cpu.hand)
            spread = min(n * 28, 400)

            for i, card in enumerate(cpu.hand):
                t = (i / max(n - 1, 1)) - 0.5 if n > 1 else 0
                if py > SCREEN_H - 200:  # Top
                    card.target_x = px + t * spread
                    card.target_y = py
                else:  # Sides
                    card.target_x = px
                    card.target_y = py + t * spread

        # 3. Update Discard Pile targets
        cx, cy = SCREEN_W // 2 + 55, SCREEN_H // 2
        for i, card in enumerate(self.discard):
            offset = min(i, 2) * 6  # Only fan out the top few cards slightly
            card.target_x = cx + offset
            card.target_y = cy + offset

    def _draw_discard(self):
        # Draw the top 3 cards at their physical animated coordinates
        for card in self.discard[-3:]:
            draw_card(card, card.x, card.y, face_up=True)

        # Keep the base coordinates just to position the "DISCARD" text label
        # cx, cy = SCREEN_W // 2 + 55, SCREEN_H // 2
        # arcade.draw_text("DISCARD", cx, cy - CARD_H // 2 - 14,
        #                  arcade.color.Color(200, 200, 200),
        #                  font_size=9, anchor_x="center")

    def _draw_deck_pile(self):
        cx, cy = SCREEN_W // 2 - 55, SCREEN_H // 2
        for i in range(min(5, len(self.deck))):
            draw_card(None, cx + i * 1.5, cy + i * 1.5, face_up=False)
        arcade.draw_text(f"DECK ({len(self.deck)})", cx + 3, cy - CARD_H // 2 - 25,
                         arcade.color.Color(200, 200, 200),
                         font_size=9,font_name=GAME_FONT, anchor_x="center")

    def _draw_cpu_hands(self):
        positions = [
            (80, SCREEN_H // 2),  # Left Bot
            (SCREEN_W // 2, SCREEN_H - 80),  # Top Bot
            (SCREEN_W - 80, SCREEN_H // 2),  # Right Bot
        ]

        for idx, player in enumerate(self.players[1:], 1):
            if idx - 1 >= len(positions):
                break

            px, py = positions[idx - 1]
            n = len(player.hand)
            is_current = (self.current_idx == idx)

            # Just draw the cards at their animated physical coordinates
            for card in player.hand:
                draw_card(card, card.x, card.y, face_up=False)

            # Draw the yellow turn indicator ring
            # if is_current:
            #     arcade.draw_ellipse_outline(px, py - 70 if py > 400 else py,
            #                                 60, 20, arcade.color.YELLOW, 3)

            # Construct the name label
            label = f"{player.name}  [{n}]"
            if player.hand and len(player.hand) == 1:
                label += " UNO!"

            # Anchor text correctly based on screen position
            if py > 400:  # Top Bot
                anchor = "center"
                text_y = py - (CARD_H // 2 + 30)
                text_x = px
            elif px < 400:  # Left Bot
                anchor = "left"
                text_y = py
                text_x = px + 55
            else:  # Right Bot
                anchor = "right"
                text_y = py
                text_x = px - 55

            is_their_turn = (self.current_idx == idx)

            if is_their_turn:
                # math.sin goes from -1 to 1. This math normalizes it to bounce between 0 and 1
                pulse = (math.sin(self.total_time * 6) + 1) / 2

                # Pulse from White (255, 255, 255) to bright Yellow (255, 255, 0)
                blue_channel = int(255 - (255 * pulse))
                text_color = arcade.color.Color(255, 255, blue_channel)
            else:
                # Dim gray if it's not their turn
                text_color = arcade.color.Color(180, 180, 180)

            # Draw the bot's name
            arcade.draw_text(
                f"{player.name}  [{len(player.hand)}]",
                text_x, text_y,
                text_color,
                font_size=12,
                anchor_x=anchor,
                font_name=GAME_FONT
            )

    def _draw_player_hand(self):
        player = self.players[0]
        n = len(player.hand)
        if n == 0:
            return

        is_my_turn = (self.current_idx == 0 and self.state == STATE_PLAYER_TURN)

        for i, card in enumerate(player.hand):
            hover = (self.hover_idx == i) and is_my_turn
            selected = (self.selected_idx == i)
            playable = card.can_play_on(self.top_card) if is_my_turn else False

            draw_card(card, card.x, card.y, face_up=True,
                      hover=hover, selected=selected)

            # --- UPDATED DIMMING LOGIC ---
            # Dim the card if it's NOT your turn, OR if it's unplayable
            if not is_my_turn or not playable:
                arcade.draw_rect_filled(
                    arcade.XYWH(card.x, card.y, CARD_W, CARD_H),
                    arcade.color.Color(0, 0, 0, 120)  # You can increase 120 to make it darker
                )

        # Player name
        arcade.draw_text(f"{player.name}  [{n}]" + (" UNO!" if n == 1 else ""),
                         SCREEN_W // 2, 150,
                         arcade.color.Color(230, 230, 230),
                         font_size=12, anchor_x="center", font_name=GAME_FONT,)

    def _draw_hud(self):
        name = self.current_player.name
        turn_txt = f"{name}'s turn"
        arcade.draw_text(turn_txt, 40, SCREEN_H - 80,
                         arcade.color.Color(240, 220, 80),
                         font_size=20, font_name=GAME_FONT)

        # dir_sym = "⟳ Clockwise" if self.direction == 1 else "⟲ Counter-CW"
        # arcade.draw_text(dir_sym, SCREEN_W - 10, SCREEN_H - 30,
        #                  arcade.color.Color(180, 220, 180),
        #                  font_size=11, anchor_x="right")

        if self.message and self.message_timer > 0:
            alpha = min(255, int(255 * self.message_timer / 2.0))
            arcade.draw_text(self.message,
                             SCREEN_W // 2, SCREEN_H // 2 + 160,
                             arcade.color.Color(255, 240, 100, alpha),
                             font_size=22, font_name=GAME_FONT, anchor_x="center")

        if self.current_idx == 0 and self.state == STATE_PLAYER_TURN:
            arcade.draw_text("Click a card to play • Click deck to draw",
                             SCREEN_W // 2, SCREEN_H // 30 + 160,
                             arcade.color.Color(150, 200, 150),
                             font_size=10, font_name=GAME_FONT, anchor_x="center")

        elif self.state == STATE_CPU_THINKING:
            arcade.draw_text(f"{self.current_player.name} is thinking…",
                             SCREEN_W // 2, SCREEN_H // 2 + 90,
                             arcade.color.Color(180, 180, 180),
                             font_size=10, font_name=GAME_FONT, anchor_x="center")
                             
        arcade.draw_text("Press ESC to Pause", 10, 15, 
                         arcade.color.WHITE, 12, font_name=GAME_FONT)

    def _draw_color_picker(self):
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_W // 2, SCREEN_H // 2,
                                            SCREEN_W, SCREEN_H),
                                arcade.color.Color(0, 0, 0, 160))

        arcade.draw_text("Choose a color", SCREEN_W // 2, SCREEN_H // 2 + 90,
                         arcade.color.Color(255, 240, 100),
                         font_size=22, font_name=GAME_FONT, anchor_x="center")

        colors = ["red", "yellow", "green", "blue"]
        for i, c in enumerate(colors):
            cx = SCREEN_W // 2 - 90 + i * 60
            cy = SCREEN_H // 2 + 20
            arcade.draw_circle_filled(cx, cy, 24, arcade.color.Color(*SUIT_COLORS[c]))
            arcade.draw_circle_outline(cx, cy, 24, arcade.color.Color(*OUTLINE_COLOR), 2)
            arcade.draw_text(c[0].upper(), cx, cy,
                             arcade.color.Color(255, 255, 255),
                             font_size=14, font_name=GAME_FONT, anchor_x="center", anchor_y="center")

    def _draw_game_over(self):
        arcade.draw_rect_filled(arcade.XYWH(SCREEN_W // 2, SCREEN_H // 2,
                                            SCREEN_W, SCREEN_H),
                                arcade.color.Color(0, 0, 0, 200))
        arcade.draw_text("GAME OVER",
                         SCREEN_W // 2, SCREEN_H // 2 + 60,
                         arcade.color.Color(255, 230, 50),
                         font_size=36, font_name=GAME_FONT, anchor_x="center")
        arcade.draw_text(f"{self.winner.name} wins!",
                         SCREEN_W // 2, SCREEN_H // 2,
                         arcade.color.Color(255, 255, 255),
                         font_size=24, font_name=GAME_FONT, anchor_x="center")
        arcade.draw_text("Press R to restart",
                         SCREEN_W // 2, SCREEN_H // 2 - 50,
                         arcade.color.Color(180, 180, 180),
                         font_size=16, font_name=GAME_FONT, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        # 1. Early exit if it's not the player's turn
        if self.state != STATE_PLAYER_TURN or self.current_idx != 0:
            self.hover_idx = None
            return

        # 2. Save the card we were hovering over during the LAST frame
        old_hover_idx = self.hover_idx

        # 3. Figure out what card we are hovering over RIGHT NOW
        self.hover_idx = self._card_idx_at(x, y)

        # 4. Play the sound ONLY if we moved onto a new card
        # (We check `is not None` so it doesn't play a sound when moving off a card onto the empty table)
        if self.hover_idx is not None and self.hover_idx != old_hover_idx:
            arcade.play_sound(self.sound_hover, volume=0.2)

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.state == STATE_GAME_OVER:
            return

        # 1. COLOR PICKER MENU
        if self.state == STATE_PICK_COLOR:
            colors = ["red", "yellow", "green", "blue"]
            for i, c in enumerate(colors):
                cx = SCREEN_W // 2 - 90 + i * 60
                cy = SCREEN_H // 2 + 20
                if math.hypot(x - cx, y - cy) < 28:
                    # --- NEW: Play a sound when selecting a wild color ---
                    self.play_sfx(self.sound_play)
                    self._finish_wild(c)
            return

        if self.state != STATE_PLAYER_TURN or self.current_idx != 0:
            return

        # 2. DRAWING FROM THE DECK
        deck_cx, deck_cy = SCREEN_W // 2 - 55, SCREEN_H // 2
        if (abs(x - deck_cx) < CARD_W // 2 + 10 and
                abs(y - deck_cy) < CARD_H // 2 + 10) :
            if not self.drew_this_turn:
                # --- NEW: Play the draw sound ---
                self.play_sfx(self.sound_draw)
                self._human_draw()
            return

        # 3. PLAYING A CARD FROM HAND
        idx = self._card_idx_at(x, y)
        if idx is not None:
            card = self.players[0].hand[idx]
            if card.can_play_on(self.top_card):

                # --- NEW: Check what kind of card it is! ---
                val = str(card.value).lower()
                if "draw" in val or "+" in val:
                    self.play_sfx(self.sound_play)
                    # It's an attack! Play the draw sound
                    self.play_sfx(self.sound_draw)
                else:
                    # It's a normal card! Play the standard snap
                    self.play_sfx(self.sound_play)

                self._human_play(idx)
    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self._setup()
        elif key == arcade.key.ESCAPE:
            pause_view = PauseMenuView(self)
            self.window.show_view(pause_view)

    def _card_idx_at(self, mx: float, my: float) -> Optional[int]:
        player = self.players[0]
        n = len(player.hand)
        if n == 0:
            return None
        spread = min(n * (CARD_W + 6), SCREEN_W - 160)
        start_x = SCREEN_W // 2 - spread // 2 + CARD_W // 2
        cy = 70

        for i in range(n - 1, -1, -1):
            cx = start_x + i * (spread // max(n - 1, 1)) if n > 1 else SCREEN_W // 2
            if (abs(mx - cx) < CARD_W // 2 and
                    abs(my - cy) < CARD_H // 2 + 20):
                return i
        return None

    def _human_play(self, idx: int):
        card = self.players[0].hand[idx]
        self._play_card(self.players[0], card)

    def _human_draw(self):
        player = self.players[0]
        drawn = self._draw_one(player)
        self.drew_this_turn = True
        if drawn and drawn.can_play_on(self.top_card):
            self._show_message(f"Drew {_card_label(drawn.value)} — you may play it!")
        else:
            self._show_message("Drew a card — no play, passing")
            self._advance_turn()
            self._queue_next_turn()

    def _cpu_play(self):
        player = self.current_player
        playable = player.playable_cards(self.top_card)
        if playable:
            playable.sort(key=lambda c: (0 if c.is_action else 1,
                                         -int(c.value) if c.value.isdigit() else 0))
            card = playable[0]
            val = str(card.value).lower()
            if "draw" in val or "+" in val:
                self.play_sfx(self.sound_play)
                self.play_sfx(self.sound_draw)
            else:
                self.play_sfx(self.sound_play)

            self._play_card(player, card)
        else:
            self.play_sfx(self.sound_draw)
            drawn = self._draw_one(player)
            if drawn and drawn.can_play_on(self.top_card):
                self.play_sfx(self.sound_play)
                self._play_card(player, drawn)
            else:
                self._show_message(f"{player.name} draws & passes")
                self._advance_turn()
                self._queue_next_turn()

    def _play_card(self, player: Player, card: Card):
        player.remove_card(card)
        self.discard.append(card)

        # --- ANIMATION TARGET POINT ---
        # The update_card_targets() function will automatically
        # tell this card to fly to the discard pile now!
        self.update_card_targets()

        self._show_message(f"{player.name} plays {_card_label(card.value)}")

        if len(player.hand) == 0:
            self.winner = player
            self.state = STATE_GAME_OVER
            return

        if len(player.hand) == 1:
            self._show_message(f" UNO! — {player.name}")

        if card.value == "skip":
            self._advance_turn()
            self._show_message(f"{self.current_player.name} is skipped!")
            self._advance_turn()
        elif card.value == "reverse":
            self.direction *= -1
            self._show_message("Direction reversed!")
            self._advance_turn()
        elif card.value == "draw2":
            self._advance_turn()
            next_p = self.current_player
            self._draw_one(next_p)
            self._draw_one(next_p)
            self._show_message(f"{next_p.name} draws 2!")
            self._advance_turn()
        elif card.value in ("wild", "wild4"):
            if player.is_human:
                self.state = STATE_PICK_COLOR
                self.selected_idx = None
                return
            else:
                chosen = self._cpu_pick_color(player)
                card.chosen_color = chosen
                self._show_message(f"{player.name} picks {chosen}")
                if card.value == "wild4":
                    self._advance_turn()
                    next_p = self.current_player
                    for _ in range(4):
                        self._draw_one(next_p)
                    self._show_message(f"{next_p.name} draws 4!")
                    self._advance_turn()
                else:
                    self._advance_turn()
        else:
            self._advance_turn()

        self._queue_next_turn()

    def _finish_wild(self, chosen_color: str):
        card = self.discard[-1]
        card.chosen_color = chosen_color
        self._show_message(f"You pick {chosen_color}")
        if card.value == "wild4":
            self._advance_turn()
            next_p = self.current_player
            for _ in range(4):
                self._draw_one(next_p)
            self._show_message(f"{next_p.name} draws 4!")
            self._advance_turn()
        else:
            self._advance_turn()
        self._queue_next_turn()

    def _advance_turn(self):
        self.current_idx = (self.current_idx + self.direction) % len(self.players)

    def _queue_next_turn(self):
        if self.state in (STATE_GAME_OVER,):
            return
        self.drew_this_turn = False
        if self.current_player.is_human:
            self.state = STATE_PLAYER_TURN
        else:
            self.state = STATE_CPU_THINKING
            self.cpu_timer = CPU_DELAY

    def _draw_one(self, player: Player) -> Optional[Card]:
        if not self.deck:
            top = self.discard.pop()
            self.deck = self.discard[:]
            random.shuffle(self.deck)
            self.discard = [top]

        if self.deck:
            card = self.deck.pop()

            # --- ANIMATION SPAWN POINT ---
            # Set the physical start position to the deck
            card.x = SCREEN_W // 2 - 55
            card.y = SCREEN_H // 2

            player.hand.append(card)

            # Recalculate targets so the new card flies to the hand
            self.update_card_targets()
            return card
        return None

    def _cpu_pick_color(self, player: Player) -> str:
        counts = {"red": 0, "yellow": 0, "green": 0, "blue": 0}
        for c in player.hand:
            if c.color in counts:
                counts[c.color] += 1
        return max(counts, key=lambda k: counts[k])

    def _show_message(self, msg: str):
        self.message = msg
        self.message_timer = 2.0

    def play_sfx(self, sound, base_vol=1.0):
        """Helper method to automatically mix SFX with the global settings"""

        # Calculate the final output volume
        final_vol = base_vol * self.window.sfx_vol * self.window.master_vol

        # Only play if the volume is above 0 (saves processing power if muted!)
        if final_vol > 0:
            arcade.play_sound(sound, volume=final_vol)