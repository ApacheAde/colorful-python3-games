#!/usr/bin/env python3
"""Neon Slots — three-reel color casino machine."""

from __future__ import annotations

import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from ansi import fg, bold

SYMBOLS = [
    ("7", 196, 12),
    ("*", 226, 8),
    ("D", 51, 6),
    ("o", 201, 5),
    ("C", 46, 4),
    ("BAR", 208, 3),
    ("c", 250, 2),
]


def pick():
    bag = []
    for name, color, w in SYMBOLS:
        bag.extend([(name, color)] * w)
    return random.choice(bag)


def frame(reels) -> None:
    print(fg(93, "    +--------+--------+--------+"))
    print(fg(93, "    |        |        |        |"))
    cells = []
    for name, color in reels:
        label = f"{name:^6}"
        cells.append(fg(color, bold(label)))
    print(fg(93, "    | ") + fg(93, " | ").join(cells) + fg(93, " |"))
    print(fg(93, "    |        |        |        |"))
    print(fg(93, "    +--------+--------+--------+") )


def payout(reels, bet: int) -> tuple[int, str]:
    names = [r[0] for r in reels]
    if names[0] == names[1] == names[2]:
        table = {"7": 25, "*": 15, "D": 10, "o": 8, "C": 6, "BAR": 5, "c": 3}
        return bet * table[names[0]], f"THREE {names[0]} -- JACKPOT PATH"
    if names[0] == names[1] or names[1] == names[2] or names[0] == names[2]:
        return bet * 2, "PAIR PAYS"
    return 0, "NO LINE"


def main() -> None:
    bank = 200
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(fg(201, "===================================="))
        print(bold(fg(226, "           * NEON SLOTS *")))
        print(fg(201, "===================================="))
        print(fg(46, f"\n  Credits ${bank}"))
        print(fg(244, "  Triple 7 pays 25x  |  any pair 2x"))
        raw = input(fg(51, "\n  Spin amount (or Q) > ")).strip()
        if raw.lower() in {"q", "quit"}:
            break
        try:
            bet = int(raw)
        except ValueError:
            continue
        if bet <= 0 or bet > bank:
            continue
        bank -= bet

        reels = [(".", 244), (".", 244), (".", 244)]
        for tick in range(14):
            if tick > 6:
                reels[0] = pick() if tick < 8 else reels[0]
            else:
                reels[0] = pick()
            if tick > 9:
                reels[1] = pick() if tick < 11 else reels[1]
            else:
                reels[1] = pick()
            reels[2] = pick()
            os.system("cls" if os.name == "nt" else "clear")
            print(fg(201, "\n        * NEON SLOTS *\n"))
            frame(reels)
            time.sleep(0.07)
        reels = [pick(), pick(), pick()]
        os.system("cls" if os.name == "nt" else "clear")
        print(fg(201, "\n        * NEON SLOTS *\n"))
        frame(reels)
        win, msg = payout(reels, bet)
        bank += win
        if win:
            print(fg(226, f"\n  {msg}  +${win}"))
        else:
            print(fg(244, f"\n  {msg}"))
        print(fg(46, f"  Credits ${bank}"))
        if bank <= 0:
            print(fg(196, "\n  Machine ate the last coin."))
            break
        input(fg(250, "\n  Enter to spin again... "))
    print(fg(201, "\n  Lights dim on the neon cabinet.\n"))


if __name__ == "__main__":
    main()
