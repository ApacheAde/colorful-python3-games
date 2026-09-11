#!/usr/bin/env python3
"""Super Plumber — colorful Mario-style side-scroller (homage, not an emulator)."""
from __future__ import annotations
import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from ansi import bg, fg, CLEAR, HIDE, SHOW, RESET

LEVEL = [
    '                                                                                          F',
    '                                                                                          #',
    '                    o                                                                     #',
    '              o           o     ####                    o                                 #',
    '         ?         ####               o        ##??##          o      ####                #',
    '                             o                                                            #',
    '    P         e        e           e        e              e         e            e       #',
    '===========================================================================================',
]
W, H, VIEW = len(LEVEL[0]), len(LEVEL), 36

def key_nonblock():
    if os.name=='nt': return ''
    import select, termios, tty
    fd=sys.stdin.fileno(); old=termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        if select.select([sys.stdin],[],[],0)[0]:
            ch=sys.stdin.read(1)
            if ch=='\x1b':
                extra=''
                if select.select([sys.stdin],[],[],0.01)[0]: extra += sys.stdin.read(1)
                if select.select([sys.stdin],[],[],0.01)[0]: extra += sys.stdin.read(1)
                return '\x1b'+extra
            return ch
        return ''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def paint(ch):
    table={
        ' ': bg(117,'  '),
        '#': bg(130, fg(223,'##')),
        '=': bg(34, fg(22,'==')),
        '?': bg(208, fg(0,'??')),
        'o': bg(117, fg(226,'o ')),
        'e': bg(117, fg(160,'e ')),
        'F': bg(117, fg(46,'F ')),
        'P': bg(117, fg(196,'@ ')),
    }
    return table.get(ch, bg(117,'  '))

def solid(ch): return ch in '#=?'

def main():
    grid=[list(row.ljust(W)) for row in LEVEL]
    px=py=0
    for y,row in enumerate(grid):
        if 'P' in row:
            px=row.index('P'); py=y; row[px]=' '; break
    vx=vy=0.0; coins=0; lives=3; won=False; facing=1
    print(HIDE, end='')
    try:
        print(CLEAR)
        print(fg(201,'SUPER PLUMBER')+'  '+fg(250,'A/D move  W jump  Q quit'))
        print(fg(244,'Coins, stomp foes, reach the green flag.'))
        time.sleep(1.0)
        while lives>0 and not won:
            k=key_nonblock()
            if os.name=='nt':
                import msvcrt
                if msvcrt.kbhit():
                    k=msvcrt.getwch()
                    if k=='\xe0':
                        k2=msvcrt.getwch()
                        k={'K':'LEFT','M':'RIGHT','H':'UP'}.get(k2,'')
            if k in ('q','Q','\x03'): break
            if k in ('a','A','\x1b[D','LEFT'): vx=-0.55; facing=-1
            elif k in ('d','D','\x1b[C','RIGHT'): vx=0.55; facing=1
            elif k in ('w','W',' ','\x1b[A','UP'):
                below = grid[py+1][int(round(px))] if py+1<H else '='
                if solid(below): vy=-1.15
            vy += 0.12
            if vy>0.95: vy=0.95
            nx=px+vx; ix,iy=int(round(nx)), py
            if 0<=ix<W and not solid(grid[iy][ix]): px=nx
            vx *= 0.72
            if abs(vx)<0.05: vx=0.0
            ny=py+vy; ix,iy2=int(round(px)), int(round(ny))
            if iy2<0: vy=0
            elif iy2>=H:
                lives-=1; px,py,vx,vy=4,6,0,0
            elif solid(grid[iy2][ix]):
                if vy>0: py=iy2-1; vy=0
                else:
                    if grid[iy2][ix]=='?':
                        grid[iy2][ix]='#'; coins+=1
                    vy=0.15; py=iy2+1
            else:
                py=iy2
            ix,iy=int(round(px)), max(0,min(H-1,int(round(py))))
            if grid[iy][ix]=='o': grid[iy][ix]=' '; coins+=1
            if grid[iy][ix]=='F': won=True
            for y in range(H):
                x=0
                while x<W:
                    if grid[y][x]=='e':
                        step = 1 if (x+int(time.time()*2))%8<4 else -1
                        nx_e=x+step
                        if 0<=nx_e<W and grid[y][nx_e]==' ' and y+1<H and solid(grid[y+1][nx_e]):
                            grid[y][x]=' '; grid[y][nx_e]='e'; x=nx_e
                        if abs(ix-x)==0 and abs(iy-y)==0:
                            if vy>0.15:
                                grid[y][x]=' '; vy=-0.7; coins+=2
                            else:
                                lives-=1; px,py,vx,vy=4,6,0,0
                    x+=1
            cam=max(0,min(W-VIEW, ix-VIEW//3))
            print(CLEAR, end='')
            print(fg(201,' SUPER PLUMBER ')+fg(226,f' COINS {coins:03d} ')+fg(196,f'LIVES {lives} ')+fg(51,f'X {ix:03d}'))
            print(fg(93,'-'*(VIEW*2)))
            for y in range(H):
                line=[]
                for x in range(cam, cam+VIEW):
                    ch=grid[y][x] if 0<=x<W else ' '
                    if x==ix and y==iy:
                        sprite='> ' if facing>0 else '< '
                        line.append(bg(117, fg(196, sprite)))
                    else:
                        line.append(paint(ch))
                print(''.join(line)+RESET)
            print(fg(93,'-'*(VIEW*2)))
            print(fg(250,'Reach the green F. Stomp foes from above.'))
            time.sleep(0.07)
        print(SHOW, end='')
        print()
        if won: print(fg(46,'WORLD CLEAR!  ')+fg(226,f'Coins {coins}'))
        else: print(fg(196,'GAME OVER  ')+fg(226,f'Coins {coins}'))
        input(fg(250,'Enter to return... '))
    finally:
        print(SHOW, end='')

if __name__ == '__main__':
    main()
