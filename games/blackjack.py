#!/usr/bin/env python3
"""Neon Blackjack — full-color casino card game."""

from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from ansi import fg, bold

SUITS = [("♥", 196), ("♦", 208), ("♣", 46), ("♠", 51)]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def deck() -> list[tuple[str, int, str]]:
    cards = [(r, s[1], s[0]) for s in SUITS for r in RANKS]
    random.shuffle(cards)
    return cards


def value(hand: list[tuple[str, int, str]]) -> int:
    total = 0
    aces = 0
    for rank, _, _ in hand:
        if rank == "A":
            aces += 1
            total += 11
        elif rank in "JQK":
            total += 10
        else:
            total += int(rank)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def card_art(card: tuple[str, int, str] | None, hidden: bool = False) -> list[str]:
    if hidden or card is None:
        return [
            fg(93, "┌─────┐"),
            fg(93, "│") + fg(201, "▒▒▒▒▒") + fg(93, "│"),
            fg(93, "│") + fg(165, "▒ ? ▒") + fg(93, "│"),
            fg(93, "│") + fg(201, "▒▒▒▒▒") + fg(93, "│"),
            fg(93, "└─────┘"),
        ]
    rank, color, suit = card
    r = f"{rank:<2}"
    r2 = f"{rank:>2}"
    return [
        fg(15, "┌─────┐"),
        fg(15, "│") + fg(color, f"{r}   ") + fg(15, "│"),
        fg(15, "│") + fg(color, f"  {suit}  ") + fg(15, "│"),
        fg(15, "│") + fg(color, f"   {r2}") + fg(15, "│"),
        fg(15, "└─────┘"),
    ]


def show(title: str, hand: list, hide_first: bool = False) -> None:
    label = "??" if hide_first else str(value(hand))
    print(fg(226, title) + fg(250, f"  ({label})"))
    arts = [card_art(c, hidden=(hide_first and i == 0)) for i, c in enumerate(hand)]
    for row in range(5):
        print("  ".join(a[row] for a in arts))


def banner(bank: int, bet: int | None = None) -> None:
    os.system("cls" if os.name == "nt" else "clear")
    print(fg(196, "╔════════════════════════════════════╗"))
    print(fg(196, "║") + bold(fg(226, "     ♠  NEON BLACKJACK  ♦         ")) + fg(196, "║"))
    print(fg(196, "║") + fg(51, "     Beat 21. Dealer stands 17.   ") + fg(196, "║"))
    print(fg(196, "╚════════════════════════════════════╝"))
    extra = f"   Bet ${bet}" if bet else ""
    print(fg(46, f"\n  Bankroll ${bank}{extra}\n"))


def settle(bank: int, bet: int, player, dealer) -> tuple[int, str]:
    pv, dv = value(player), value(dealer)
    p_bj = pv == 21 and len(player) == 2
    d_bj = dv == 21 and len(dealer) == 2
    if p_bj and not d_bj:
        return bank + int(bet * 1.5), fg(226, "  BLACKJACK pays 3:2")
    if d_bj and not p_bj:
        return bank - bet, fg(196, "  Dealer blackjack.")
    if pv > 21:
        return bank - bet, fg(196, "  BUST.")
    if dv > 21:
        return bank + bet, fg(46, "  Dealer busts. You win.")
    if pv > dv:
        return bank + bet, fg(46, "  YOU WIN.")
    if pv < dv:
        return bank - bet, fg(196, "  DEALER WINS.")
    return bank, fg(226, "  PUSH.")


def main() -> None:
    bank = 500
    while True:
        banner(bank)
        if bank <= 0:
            print(fg(196, "  Busted. The house always smiles."))
            break
        raw = input(fg(51, "  Bet (or Q quit) > ")).strip()
        if raw.lower() in {"q", "quit"}:
            break
        try:
            bet = int(raw)
        except ValueError:
            continue
        if bet <= 0 or bet > bank:
            continue

        d = deck()
        player = [d.pop(), d.pop()]
        dealer = [d.pop(), d.pop()]

        while True:
            banner(bank, bet)
            show("  DEALER", dealer, hide_first=True)
            print()
            show("  YOU", player)
            if value(player) == 21 and len(player) == 2:
                break
            if value(player) > 21:
                break
            act = input(fg(213, "\n  [H]it  [S]tand  [D]ouble  > ")).strip().lower()
            if act.startswith("d") and len(player) == 2 and bet * 2 <= bank:
                bet *= 2
                player.append(d.pop())
                break
            if act.startswith("h"):
                player.append(d.pop())
                continue
            if act.startswith("s") or act == "":
                break

        if value(player) <= 21:
            while value(dealer) < 17:
                dealer.append(d.pop())

        banner(bank, bet)
        show("  DEALER", dealer)
        print()
        show("  YOU", player)
        print()
        bank, msg = settle(bank, bet, player, dealer)
        print(msg)
        print(fg(46, f"  Bankroll now ${bank}"))
        input(fg(244, "\n  Enter to deal again... "))
    print(fg(201, "\n  Thanks for playing Neon Blackjack.\n"))


if __name__ == "__main__":
    main()
