# constants.py

SCREEN_W, SCREEN_H = 1200, 800
TITLE = "UNO — Arcade Edition"

CARD_W, CARD_H = 72, 108
CARD_RADIUS = 8
CARD_SCALE = 1.0

BG_COLOR        = (18, 28, 18)
TABLE_COLOR     = (30, 80, 45)
OUTLINE_COLOR   = (240, 230, 200)

SUIT_COLORS = {
    "red":    (220,  50,  50),
    "yellow": (230, 190,   0),
    "green":  (40,  170,  60),
    "blue":   (30,  100, 210),
    "wild":   (25,  25,  25),
}

TEXT_ON_DARK  = (240, 230, 200)
TEXT_ON_LIGHT = (20,  20,  20)

NUM_PLAYERS   = 4          # 1 human + 2 CPU
DEAL_CARDS    = 7
CPU_DELAY     = 1.2        # seconds before CPU plays

DEBUG_MODE = False