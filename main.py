from typing import Tuple

import pygame as pg

from minesweeper import Minesweeper, TILE
from ai import process_field, ACTION


class Colors:
    BG = (240, 240, 180)
    UNCOVERED = (100, 100, 80)
    FLAGGED = (120, 240, 120)
    TILE = (200, 200, 170)
    MINE = (230, 100, 100)
    TEXT = (50, 50, 50)


pg.init()
screen = pg.display.set_mode(flags=pg.FULLSCREEN)
minesweeper = Minesweeper(30, 16)
w, h = minesweeper.width, minesweeper.height
sw, sh = screen.get_size()
ts = round(
    min(
        ((sw * 0.7) / w),
        ((sh * 0.7) / h),
    )
)
font = pg.font.SysFont("", size=ts)


def world_to_field(rx, ry) -> Tuple[int, int]:
    return [
        int((rx - (sw / 2 - (w * ts / 2))) / ts),
        int((ry - (sh / 2 - (h * ts / 2))) / ts),
    ]


def handle_event(e: pg.event):
    if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
        rx, ry = e.pos
        x, y = world_to_field(rx, ry)
        minesweeper.uncover(x, y)
    if e.type == pg.MOUSEBUTTONDOWN and e.button == 3:
        rx, ry = e.pos
        x, y = world_to_field(rx, ry)
        minesweeper.flag(x, y)
    if e.type == pg.KEYDOWN:
        if e.unicode == "f":
            minesweeper.random_fill(80)
        if e.unicode == "d":
            rx, ry = pg.mouse.get_pos()
            x, y = world_to_field(rx, ry)
            minesweeper.set_mine(x, y)
        if e.unicode == "r":
            minesweeper.reset()
        if e.unicode == "c":
            minesweeper.cover()
        if e.unicode == "g":
            moves = process_field(minesweeper.field, w, h)
            for move in moves:
                if move.action == ACTION.FLAG:
                    minesweeper.flag(*move.pos)
                if move.action == ACTION.UNCOVER:
                    minesweeper.uncover(*move.pos)


def draw():
    screen.fill(Colors.BG)

    field = minesweeper.field
    for y in range(h):
        for x in range(w):
            tile = field[y][x]

            color = Colors.TILE
            text = None

            if tile == TILE.COVERED:
                color = Colors.UNCOVERED
            elif tile == TILE.FLAGGED:
                color = Colors.FLAGGED
            elif tile > 9:
                color = Colors.MINE
            else:
                text = str(tile)

            rect = [
                sw / 2 - (w * ts / 2) + x * ts + 1,
                sh / 2 - (h * ts / 2) + y * ts + 1,
                ts - 2,
                ts - 2,
            ]
            pg.draw.rect(screen, color, rect)
            if text:
                render = font.render(text, True, Colors.TEXT)
                text_pos = [
                    rect[0] + ts / 2 - render.get_width() / 2,
                    rect[1] + ts / 2 - render.get_height() / 2,
                ]
                screen.blit(render, text_pos)


clock = pg.time.Clock()
while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()
        handle_event(e)
    draw()
    pg.display.flip()
    clock.tick(60)
