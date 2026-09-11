#!/usr/bin/env python3
"""Prism Snake — colorful terminal snake."""
from __future__ import annotations
import os, random, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from ansi import fg, bg, CLEAR, HIDE, SHOW

W, H = 28, 16

def getch(timeout):
    if os.name == 'nt':
        import msvcrt
        t0 = time.time()
        while time.time() - t0 < timeout:
            if msvcrt.kbhit():
                k = msvcrt.getwch()
                if k == '\xe0':
                    k2 = msvcrt.getwch()
                    return {'K':'L','M':'R','H':'U','P':'D'}.get(k2, '')
                return k
            time.sleep(0.02)
        return ''
    import select, termios, tty
    fd = sys.stdin.fileno(); old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        r, _, _ = select.select([sys.stdin], [], [], timeout)
        if not r: return ''
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            extra = ''
            if select.select([sys.stdin], [], [], 0.01)[0]: extra += sys.stdin.read(1)
            if select.select([sys.stdin], [], [], 0.01)[0]: extra += sys.stdin.read(1)
            return {'\x1b[A':'U','\x1b[B':'D','\x1b[C':'R','\x1b[D':'L'}.get('\x1b'+extra, '')
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def main():
    snake = [(W//2, H//2), (W//2-1, H//2), (W//2-2, H//2)]
    dx, dy, score = 1, 0, 0
    def place_food():
        cells = {(x,y) for x in range(W) for y in range(H)} - set(snake)
        return random.choice(list(cells))
    food = place_food()
    print(HIDE, end='')
    try:
        while True:
            k = getch(0.12)
            if k in ('q','Q','\x03'): break
            mapping = {'a':(-1,0),'d':(1,0),'w':(0,-1),'s':(0,1),'L':(-1,0),'R':(1,0),'U':(0,-1),'D':(0,1)}
            if k in mapping:
                ndx, ndy = mapping[k]
                if (ndx, ndy) != (-dx, -dy):
                    dx, dy = ndx, ndy
            hx, hy = snake[0]
            nx, ny = hx+dx, hy+dy
            if nx<0 or nx>=W or ny<0 or ny>=H or (nx,ny) in snake:
                break
            snake.insert(0, (nx,ny))
            if (nx,ny) == food:
                score += 10; food = place_food()
            else:
                snake.pop()
            print(CLEAR, end='')
            print(fg(201,' PRISM SNAKE ') + fg(226,f' SCORE {score} ') + fg(244,'WASD / arrows  Q quit'))
            print(fg(93, '+' + '--'*W + '+'))
            body = set(snake)
            for y in range(H):
                row = [fg(93,'|')]
                for x in range(W):
                    if (x,y) == snake[0]:
                        row.append(bg(201, fg(15,'@@')))
                    elif (x,y) in body:
                        idx = snake.index((x,y))
                        pal = [129,93,63,39,45,50]
                        row.append(bg(pal[idx % len(pal)], '  '))
                    elif (x,y) == food:
                        row.append(bg(0, fg(226,'* ')))
                    else:
                        row.append(bg(16,'  '))
                row.append(fg(93,'|'))
                print(''.join(row))
            print(fg(93, '+' + '--'*W + '+'))
    finally:
        print(SHOW, end='')
    print(fg(196, f'\n  CRASH. Score {score}'))
    input(fg(244, '  Enter to return... '))

if __name__ == '__main__':
    main()
