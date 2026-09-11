"""Tiny ANSI color helpers shared by the arcade pack."""

from __future__ import annotations


def fg(n: int, text: str) -> str:
    return f"\033[38;5;{n}m{text}\033[0m"


def bg(n: int, text: str) -> str:
    return f"\033[48;5;{n}m{text}\033[0m"


def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def rgb(r: int, g: int, b: int, text: str) -> str:
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


RESET = "\033[0m"
CLEAR = "\033[2J\033[H"
HIDE = "\033[?25l"
SHOW = "\033[?25h"

# Palette
GOLD = 220
RED = 196
GREEN = 46
CYAN = 51
MAGENTA = 201
BLUE = 39
ORANGE = 208
PINK = 213
WHITE = 15
GRAY = 244
BROWN = 130
SKY = 117
GRASS = 34
COIN = 226
ENEMY = 160
PLAYER = 196
