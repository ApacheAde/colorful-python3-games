#!/usr/bin/env python3
"""Connect Four — colorful human vs CPU (minimax)."""
from __future__ import annotations
import os, random, sys
sys.path.insert(0, os.path.dirname(__file__))
from ansi import fg, bg, bold

ROWS, COLS = 6, 7
HUMAN, CPU = 'X', 'O'

def empty(): return [['.']*COLS for _ in range(ROWS)]

def drop(board, col, piece):
    for r in range(ROWS-1,-1,-1):
        if board[r][col]=='.':
            board[r][col]=piece; return r
    return None

def undo(board, col):
    for r in range(ROWS):
        if board[r][col]!='.':
            board[r][col]='.'; return

def winner(board):
    def line(a,b,c,d): return a==b==c==d and a!='.'
    for r in range(ROWS):
        for c in range(COLS):
            p=board[r][c]
            if p=='.': continue
            if c+3<COLS and line(p,board[r][c+1],board[r][c+2],board[r][c+3]): return p
            if r+3<ROWS and line(p,board[r+1][c],board[r+2][c],board[r+3][c]): return p
            if r+3<ROWS and c+3<COLS and line(p,board[r+1][c+1],board[r+2][c+2],board[r+3][c+3]): return p
            if r+3<ROWS and c-3>=0 and line(p,board[r+1][c-1],board[r+2][c-2],board[r+3][c-3]): return p
    return None

def full(board): return all(board[0][c]!='.' for c in range(COLS))
def legal(board): return [c for c in range(COLS) if board[0][c]=='.']

def score_window(window, piece):
    opp = HUMAN if piece==CPU else CPU
    s=0
    if window.count(piece)==4: s+=100
    elif window.count(piece)==3 and window.count('.')==1: s+=8
    elif window.count(piece)==2 and window.count('.')==2: s+=2
    if window.count(opp)==3 and window.count('.')==1: s-=12
    return s

def evaluate(board, piece):
    total = [board[r][COLS//2] for r in range(ROWS)].count(piece)*3
    for r in range(ROWS):
        for c in range(COLS-3): total += score_window(board[r][c:c+4], piece)
    for c in range(COLS):
        col=[board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3): total += score_window(col[r:r+4], piece)
    for r in range(ROWS-3):
        for c in range(COLS-3): total += score_window([board[r+i][c+i] for i in range(4)], piece)
        for c in range(3,COLS): total += score_window([board[r+i][c-i] for i in range(4)], piece)
    return total

def minimax(board, depth, alpha, beta, maximizing):
    w = winner(board)
    if w==CPU: return None, 10000+depth
    if w==HUMAN: return None, -10000-depth
    moves = legal(board)
    if not moves or depth==0: return None, evaluate(board, CPU)
    best = random.choice(moves)
    if maximizing:
        value=-10**9
        for col in moves:
            drop(board,col,CPU); _,score=minimax(board,depth-1,alpha,beta,False); undo(board,col)
            if score>value: value,best=score,col
            alpha=max(alpha,value)
            if alpha>=beta: break
        return best,value
    value=10**9
    for col in moves:
        drop(board,col,HUMAN); _,score=minimax(board,depth-1,alpha,beta,True); undo(board,col)
        if score<value: value,best=score,col
        beta=min(beta,value)
        if alpha>=beta: break
    return best,value

def draw(board):
    print(fg(51,'\n    1   2   3   4   5   6   7'))
    print(fg(25,'  +---+---+---+---+---+---+---+'))
    for r,row in enumerate(board):
        cells=[]
        for cell in row:
            if cell=='X': cells.append(bg(196, fg(15,' O ')))
            elif cell=='O': cells.append(bg(226, fg(0,' O ')))
            else: cells.append(bg(17,'   '))
        print(fg(25,'  |') + fg(25,'|').join(cells) + fg(25,'|'))
        if r<ROWS-1: print(fg(25,'  +---+---+---+---+---+---+---+'))
    print(fg(25,'  +---+---+---+---+---+---+---+'))

def main():
    board=empty()
    os.system('cls' if os.name=='nt' else 'clear')
    print(fg(39, bold('     CONNECT FOUR  vs CPU')))
    print(fg(250,'     You are RED  |  CPU is GOLD'))
    print(fg(244,'  Inspired by the live board on x.com/ElbowOS'))
    turn=HUMAN
    while True:
        draw(board)
        w=winner(board)
        if w==HUMAN: print(fg(46,'\n  YOU CONNECT FOUR.')); break
        if w==CPU: print(fg(196,'\n  CPU CONNECTS FOUR.')); break
        if full(board): print(fg(226,'\n  DRAW.')); break
        if turn==HUMAN:
            raw=input(fg(51,'  Column 1-7 (Q quit) > ')).strip().lower()
            if raw in {'q','quit'}: break
            if not raw.isdigit() or not (1<=int(raw)<=7): continue
            col=int(raw)-1
            if drop(board,col,HUMAN) is None:
                print(fg(196,'  Column full.')); continue
            turn=CPU
        else:
            print(fg(226,'  CPU thinking...'))
            col,_=minimax(board,5,-10**9,10**9,True)
            drop(board, col if col is not None else legal(board)[0], CPU)
            print(fg(226, f'  CPU drops in column {col+1}'))
            turn=HUMAN
    input(fg(244,'\n  Enter to return... '))

if __name__ == '__main__':
    main()
