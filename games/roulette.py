#!/usr/bin/env python3
"""Roulette Royale — European wheel in full color."""
from __future__ import annotations
import os, random, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from ansi import fg, bold

WHEEL = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]
RED = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

def color_of(n):
    if n == 0: return 'GREEN', 46
    if n in RED: return 'RED', 196
    return 'BLACK', 250

def paint_num(n):
    return fg(color_of(n)[1], f'{n:2d}')

def spin_anim(land):
    idx = random.randint(0, 36)
    for t in range(28):
        idx = (idx + 1) % 37
        n = WHEEL[idx]
        bar = ' '.join(paint_num(WHEEL[(idx + k) % 37]) for k in range(-3, 4))
        print('\r  ' + fg(color_of(n)[1], 'o ') + bar + fg(226, '  <'), end='', flush=True)
        time.sleep(0.03 + t * 0.008)
    target = WHEEL.index(land)
    while idx != target:
        idx = (idx + 1) % 37
        n = WHEEL[idx]
        bar = ' '.join(paint_num(WHEEL[(idx + k) % 37]) for k in range(-3, 4))
        print('\r  ' + fg(color_of(n)[1], 'o ') + bar + fg(226, '  <'), end='', flush=True)
        time.sleep(0.06)
    print()

def parse_bet(text):
    t = text.strip().lower()
    if t in {'red','r'}: return ('color','RED')
    if t in {'black','b'}: return ('color','BLACK')
    if t in {'even','e'}: return ('parity','even')
    if t in {'odd','o'}: return ('parity','odd')
    if t in {'low','1-18'}: return ('range','low')
    if t in {'high','19-36'}: return ('range','high')
    if t.isdigit() and 0 <= int(t) <= 36: return ('straight', int(t))
    return None

def pays(kind, val, n, stake):
    name,_ = color_of(n)
    if kind == 'straight' and val == n: return stake * 35
    if kind == 'color' and name == val and n != 0: return stake
    if kind == 'parity' and n != 0:
        if val == 'even' and n % 2 == 0: return stake
        if val == 'odd' and n % 2 == 1: return stake
    if kind == 'range' and n != 0:
        if val == 'low' and 1 <= n <= 18: return stake
        if val == 'high' and 19 <= n <= 36: return stake
    return -stake

def main():
    bank = 500
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(fg(196, '======== ROULETTE ROYALE  EURO 0 ========'))
        print(fg(46, f'\n  Bankroll ${bank}'))
        print(fg(244, '  Bets: 0-36 | red/black | even/odd | low/high'))
        raw = input(fg(51, '  Place bet type (or Q) > ')).strip()
        if raw.lower() in {'q','quit'}: break
        spec = parse_bet(raw)
        if not spec: continue
        try: stake = int(input(fg(51, '  Stake $ > ')).strip())
        except ValueError: continue
        if stake <= 0 or stake > bank: continue
        land = random.choice(WHEEL)
        print(); spin_anim(land)
        name, col = color_of(land)
        print(fg(col, bold(f'\n  BALL LANDS ON {land}  {name}')))
        result = pays(*spec, land, stake)
        if result > 0:
            print(fg(46, f'  WIN +${result}')); bank += result
        else:
            print(fg(196, f'  LOSE ${stake}')); bank += result
        if bank <= 0:
            print(fg(196, '\n  The croupier sweeps the felt.')); break
        input(fg(244, '\n  Enter for another spin... '))
    print(fg(201, '\n  Wheel stops.\n'))

if __name__ == '__main__':
    main()
