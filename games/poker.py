#!/usr/bin/env python3
"""Velvet Poker — colorful 5-card draw vs the house."""
from __future__ import annotations
import os, random, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from ansi import fg, bold

SUITS = [('\u2665',196),('\u2666',208),('\u2663',40),('\u2660',51)]
RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
RVAL = {r:i for i,r in enumerate(RANKS)}

def fresh_deck():
    cards = [(r,s[1],s[0]) for s in SUITS for r in RANKS]
    random.shuffle(cards)
    return cards

def render(hand):
    tops, mids, bots = [], [], []
    for i,(r,col,s) in enumerate(hand):
        tops.append(fg(col, '+-----+'))
        mids.append(fg(col, f'| {r:<2}{s} |'))
        bots.append(fg(244, f'  [{i+1}]  '))
    print('  '.join(tops))
    print('  '.join(mids))
    print('  '.join(fg(col,'+-----+') for _,col,_ in hand))
    print('  '.join(bots))

def rank_hand(hand):
    ranks = sorted((RVAL[c[0]] for c in hand), reverse=True)
    suits = [c[2] for c in hand]
    counts = Counter(ranks)
    freq = sorted(counts.values(), reverse=True)
    unique = sorted(counts, key=lambda r: (counts[r], r), reverse=True)
    flush = len(set(suits)) == 1
    straight = False
    rs = sorted(set(ranks))
    if len(rs)==5 and rs[-1]-rs[0]==4: straight = True
    if set(ranks)=={12,0,1,2,3}:
        straight = True
        unique = [3,2,1,0,-1]
    if straight and flush and max(ranks)==12: return 9, unique, 'ROYAL FLUSH'
    if straight and flush: return 8, unique, 'STRAIGHT FLUSH'
    if freq==[4,1]: return 7, unique, 'FOUR OF A KIND'
    if freq==[3,2]: return 6, unique, 'FULL HOUSE'
    if flush: return 5, unique, 'FLUSH'
    if straight: return 4, unique, 'STRAIGHT'
    if freq==[3,1,1]: return 3, unique, 'THREE OF A KIND'
    if freq==[2,2,1]: return 2, unique, 'TWO PAIR'
    if freq==[2,1,1,1]: return 1, unique, 'ONE PAIR'
    return 0, unique, 'HIGH CARD'

def main():
    bank = 500
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        print(fg(165, bold('        VELVET POKER  -  5-card draw')))
        print(fg(46, f'\n  Bankroll ${bank}'))
        raw = input(fg(51, '  Ante (or Q) > ')).strip()
        if raw.lower() in {'q','quit'}: break
        try: ante = int(raw)
        except ValueError: continue
        if ante<=0 or ante>bank: continue
        d = fresh_deck()
        you = [d.pop() for _ in range(5)]
        house = [d.pop() for _ in range(5)]
        os.system('cls' if os.name=='nt' else 'clear')
        print(fg(225, '\n  YOUR HAND')); render(you)
        print(fg(244, '\n  Type card numbers to discard (e.g. 1 3 5), or Enter to keep.'))
        raw = input(fg(213, '  Discard > ')).strip()
        toss=[]
        for tok in raw.replace(',',' ').split():
            if tok.isdigit() and 1<=int(tok)<=5: toss.append(int(tok)-1)
        for i in sorted(set(toss), reverse=True):
            you[i] = d.pop()
        hs,_,_ = rank_hand(house)
        if hs==0:
            order = sorted(range(5), key=lambda i: RVAL[house[i][0]])
            for i in order[:3]: house[i] = d.pop()
        ys,yk,yn = rank_hand(you)
        hs,hk,hn = rank_hand(house)
        os.system('cls' if os.name=='nt' else 'clear')
        print(fg(196,'  HOUSE')); render(house); print(fg(208,f'  {hn}\n'))
        print(fg(46,'  YOU')); render(you); print(fg(226,f'  {yn}\n'))
        if (ys,yk)>(hs,hk):
            print(fg(46,f'  YOU WIN  +${ante}')); bank += ante
        elif (ys,yk)<(hs,hk):
            print(fg(196,f'  HOUSE WINS  -${ante}')); bank -= ante
        else:
            print(fg(226,'  SPLIT POT'))
        if bank<=0:
            print(fg(196,'\n  Felt is empty.')); break
        input(fg(244,'\n  Enter for another hand... '))
    print(fg(225,'\n  The velvet table goes dark.\n'))

if __name__ == '__main__':
    main()
