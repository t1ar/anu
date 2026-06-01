# models.py

import arcade
import random
from typing import Optional
from constants import *
from PIL import Image

TEXTURE_CACHE = {}


def get_card_texture(color, value, face_up: bool):
    # 1. Determine the exact filename
    if not face_up:
        filename = "assets/cards/card_back.png"
    elif color == "wild":
        # Unplayed wild cards look for "assets/cards/wild.png"
        filename = f"assets/cards/{value}.png"
    else:
        # This now handles BOTH normal cards (e.g. "red_0.png")
        # AND played wilds (e.g. "red_wild.png")
        filename = f"assets/cards/{color}_{value}.png"

    # 2. Check memory cache
    if filename in TEXTURE_CACHE:
        return TEXTURE_CACHE[filename]

    # 3. Load from disk with your custom fallback
    try:
        texture = arcade.load_texture(filename)
        TEXTURE_CACHE[filename] = texture
        return texture
    except FileNotFoundError:
        print(f"MISSING ASSET: Could not find '{filename}'. Loading assets/missing.png")
        try:
            fallback = arcade.load_texture("assets/missing.png")
        except FileNotFoundError:
            from PIL import Image
            img = Image.new("RGBA", (int(CARD_W), int(CARD_H)), color=(255, 0, 255, 255))
            fallback = arcade.Texture("fallback_magenta", img)

        TEXTURE_CACHE[filename] = fallback
        return fallback

class Card:
    SPECIALS = {"skip", "reverse", "draw2", "wild", "wild4"}

    def __init__(self, color: str, value: str):
        self.color = color      
        self.value = value      
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        self.angle = 0.0
        self.face_up = True
        self.hover = False
        self.chosen_color: Optional[str] = None

    def update(self):
        # Linear interpolation (Lerp)
        # Moves the card 10% of the distance to its target every frame
        speed = 0.10

        # Snap to target if it's very close to stop micro-stuttering
        if abs(self.target_x - self.x) < 0.5 and abs(self.target_y - self.y) < 0.5:
            self.x = self.target_x
            self.y = self.target_y
        else:
            self.x += (self.target_x - self.x) * speed
            self.y += (self.target_y - self.y) * speed

    @property
    def is_wild(self):
        return self.value in ("wild", "wild4")

    @property
    def is_action(self):
        return self.value in self.SPECIALS

    @property
    def display_color(self):
        if self.is_wild and self.chosen_color:
            return self.chosen_color
        return self.color

    def can_play_on(self, top: "Card") -> bool:
        effective_top_color = top.chosen_color if top.is_wild else top.color
        if self.is_wild:
            return True
        if self.color == effective_top_color:
            return True
        if self.value == top.value:
            return True
        return False

    def __repr__(self):
        return f"Card({self.color},{self.value})"


class Player:
    def __init__(self, name: str, is_human: bool):
        self.name = name
        self.is_human = is_human
        self.hand: list[Card] = []
        self.won: bool = False

    def playable_cards(self, top: Card) -> list[Card]:
        return [c for c in self.hand if c.can_play_on(top)]

    def remove_card(self, card: Card):
        self.hand.remove(card)


def build_deck() -> list[Card]:
    deck = []
    colors = ["red", "yellow", "green", "blue"]
    for color in colors:
        deck.append(Card(color, "0"))
        for val in ["1","2","3","4","5","6","7","8","9",
                    "skip","reverse","draw2"]:
            deck.append(Card(color, val))
            deck.append(Card(color, val))
    for _ in range(4):
        deck.append(Card("wild", "wild"))
        deck.append(Card("wild", "wild4"))
    random.shuffle(deck)
    return deck


def draw_rounded_rect(cx, cy, w, h, r, color, outline=None, outline_w=2):
    arcade.draw_rect_filled(
        arcade.XYWH(cx, cy, w, h),
        arcade.color.Color(*color),
    )
    if outline:
        arcade.draw_rect_outline(
            arcade.XYWH(cx, cy, w, h),
            arcade.color.Color(*outline),
            outline_w,
        )


def _card_label(value: str) -> str:
    return {
        "skip": "⊘", "reverse": "↺",
        "draw2": "+2", "wild": "W", "wild4": "W+4",
    }.get(value, value)


def draw_card(card, cx: float, cy: float, face_up=True, hover=False, selected=False):
    scale = 1.08 if hover else 1.0
    w = CARD_W * scale
    h = CARD_H * scale

    if card is None or not face_up:
        texture = get_card_texture(None, None, face_up=False)
    else:
        # Check if the card is a wild that has been assigned a color!
        if card.is_wild and card.chosen_color:
            effective_color = card.chosen_color
        else:
            effective_color = card.color

        texture = get_card_texture(effective_color, card.value, face_up)

    # Draw a shadow beneath the card
    arcade.draw_rect_filled(
        arcade.XYWH(cx + 4, cy - 4, w, h),
        arcade.color.Color(0, 0, 0, 80)
    )

    # Draw the actual image
    arcade.draw_texture_rect(
        texture,
        arcade.XYWH(cx, cy, w, h)
    )