# models.py

import arcade
import random
from typing import Optional
from constants import *

TEXTURE_CACHE = {}


def get_card_texture(color: str, value: str, face_up: bool):
    """Loads a texture from disk or retrieves it from the cache."""

    if not face_up:
        filename = "assets/cards/back.png"
    elif value in ("wild", "wild4"):
        filename = f"assets/cards/{value}.png"
    else:
        filename = f"assets/cards/{color}_{value}.png"

    # If we already loaded this image, return it instantly
    if filename in TEXTURE_CACHE:
        return TEXTURE_CACHE[filename]

    # Otherwise, load it from the hard drive and save it to the cache
    try:
        texture = arcade.load_texture(filename)
        TEXTURE_CACHE[filename] = texture
        return texture
    except FileNotFoundError:
        # Fallback if you forgot an image file!
        print(f"Warning: Could not find {filename}")
        # Return a default texture or let it crash so you can fix it
        return arcade.load_texture(":resources:images/test_textures/error.png")

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

    # FIX: Safely handle when 'card' is None (like the deck pile)
    if card is None or not face_up:
        texture = get_card_texture(None, None, face_up=False)
    else:
        texture = get_card_texture(card.color, card.value, face_up)

    # Draw a shadow beneath the card
    arcade.draw_rect_filled(
        arcade.XYWH(cx + 4, cy - 4, w, h),
        arcade.color.Color(0, 0, 0, 80)
    )

    # Draw the actual image using Arcade 3.0 syntax
    arcade.draw_texture_rect(
        texture,
        arcade.XYWH(cx, cy, w, h)
    )

    # FIX: Make sure 'card' actually exists before checking if it's wild
    if face_up and card and card.is_wild and card.chosen_color:
        indicator_color = SUIT_COLORS[card.chosen_color]
        arcade.draw_circle_filled(cx, cy + h / 2 + 10, 8, arcade.color.Color(*indicator_color))
        arcade.draw_circle_outline(cx, cy + h / 2 + 10, 8, arcade.color.WHITE, 2)