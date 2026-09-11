#!/usr/bin/env python3
"""Colorful Python 3 Games — launcher menu."""

from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GAMES = os.path.join(ROOT, "games")

MENU = [
    ("1", "Super Plumber  (Mario-style platformer)", "plumber.py"),
    ("2", "Neon Blackjack (casino cards)", "blackjack.py"),
    ("3", "Velvet Poker   (5-card draw)", "poker.py"),
    ("4", "Neon Slots     (casino)", "slots.py"),
    ("5", "Roulette Royale (European wheel)", "roulette.py"),
    ("6", "Prism Snake    (arcade)", "snake.py"),
    ("7", "Connect Four   (vs CPU)", "connect_four.py"),
]


def c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m"


def main() -> None:
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(c("1;95", "╔══════════════════════════════════════════════╗"))
        print(c("1;95", "║") + c("1;97", "     COLORFUL PYTHON 3 ARCADE               ") + c("1;95", "║"))
        print(c("1;95", "║") + c("96", "     x.com/ElbowOS  ·  python3 only         ") + c("1;95", "║"))
        print(c("1;95", "╚══════════════════════════════════════════════╝"))
        print()
        for key, title, _ in MENU:
            print(f"  {c('1;93', key)})  {c('1;97', title)}")
        print(f"  {c('1;91', 'Q')})  Quit")
        print()
        choice = input(c("1;92", "  Select game > ")).strip().lower()
        if choice in {"q", "quit", "exit"}:
            print(c("1;96", "\n  See you at the neon grid.\n"))
            return
        match = next((item for item in MENU if item[0] == choice), None)
        if not match:
            continue
        path = os.path.join(GAMES, match[2])
        subprocess.call([sys.executable, path])


if __name__ == "__main__":
    main()
