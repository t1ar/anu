# models.py

import arcade
import random
from typing import Optional
from constants import *

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


def draw_card(card: Card, cx: float, cy: float, face_up=True, hover=False, selected=False):
    scale = 1.08 if hover else 1.0
    w = CARD_W * scale
    h = CARD_H * scale

    if not face_up:
        draw_rounded_rect(cx, cy, w, h, CARD_RADIUS,
                          (15, 40, 80), OUTLINE_COLOR, 2)
        draw_rounded_rect(cx, cy, w * 0.6, h * 0.75, CARD_RADIUS - 2,
                          (200, 20, 20), None)
        arcade.draw_text("UNO", cx, cy,
                         arcade.color.Color(255, 220, 0),
                         bold=True, font_size=13,
                         anchor_x="center", anchor_y="center")
        return

    bg = SUIT_COLORS[card.color]
    eff = card.chosen_color if (card.is_wild and card.chosen_color) else card.color
    eff_bg = SUIT_COLORS[eff]

    # Shadow
    draw_rounded_rect(cx + 3, cy - 3, w, h, CARD_RADIUS, (0, 0, 0, 80))

    # Main body
    draw_rounded_rect(cx, cy, w, h, CARD_RADIUS, eff_bg,
                      (255, 255, 180) if selected else OUTLINE_COLOR, 3 if selected else 2)

    # Inner oval
    arcade.draw_ellipse_filled(cx, cy, w * 0.72, h * 0.55, arcade.color.Color(255, 255, 255, 60))

    # Label
    label = _card_label(card.value)
    font_size = 22 if len(label) == 1 else 14
    txt_color = TEXT_ON_DARK if eff in ("blue", "wild") else TEXT_ON_LIGHT

    arcade.draw_text(label, cx, cy,
                     arcade.color.Color(*txt_color),
                     bold=True, font_size=font_size,
                     anchor_x="center", anchor_y="center")

    # Corner pips
    corner_size = 10
    for dx, dy in [(-w/2 + 10, h/2 - 10), (w/2 - 10, -h/2 + 10)]:
        arcade.draw_text(label, cx + dx, cy + dy,
                         arcade.color.Color(*txt_color),
                         bold=True, font_size=corner_size,
                         anchor_x="center", anchor_y="center")