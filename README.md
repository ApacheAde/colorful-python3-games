# Colorful Python 3 Games

A pack of **distinct**, **full-color** terminal games written for **Python 3**.  
No extra packages required — just `python3`. Colors use ANSI / 256-color codes.

Featured alongside **[ElbowOS on X](https://x.com/ElbowOS)**.

Repo: https://github.com/ApacheAde/colorful-python3-games

## Games

| Game | File | Genre | How to run |
|------|------|-------|------------|
| Super Plumber | `games/plumber.py` | Mario-style platformer | `python3 games/plumber.py` |
| Neon Blackjack | `games/blackjack.py` | Casino card game | `python3 games/blackjack.py` |
| Velvet Poker | `games/poker.py` | 5-card draw | `python3 games/poker.py` |
| Neon Slots | `games/slots.py` | Casino slots | `python3 games/slots.py` |
| Roulette Royale | `games/roulette.py` | European roulette | `python3 games/roulette.py` |
| Prism Snake | `games/snake.py` | Arcade snake | `python3 games/snake.py` |
| Connect Four | `games/connect_four.py` | Board game vs CPU | `python3 games/connect_four.py` |

Or launch the menu:

```bash
python3 play.py
```

## Requirements

- Python 3.8+
- A terminal that supports ANSI colors (most modern terminals, Windows Terminal, macOS Terminal, iTerm, gnome-terminal)
- Unix-like key input for the action games (Linux / macOS). On Windows, snake and plumber fall back to Enter-based controls.

## Notes

These are **original simple games**, not ROM emulators. A real Mario Bros emulator is a large project (6502 CPU + PPU + mappers). Super Plumber is a colorful side-scrolling homage with jump, gravity, coins, and goombas.

## License

MIT
