from typing import List
from random import randint


class TILE:
    COVERED = -1
    FLAGGED = -2


class Minesweeper:
    def __init__(
        self,
        width: int,
        height: int,
    ):
        self.width = width
        self.height = height
        self.mine_count = 0

        self._uncovered = self._gen_filled_grid()
        self._flagged = self._gen_filled_grid()
        self._field = self._gen_filled_grid()

        self._field_cache = None
        self._updated = True

    @property
    def field(self) -> List[List[int]]:
        if self._updated:
            output = self._gen_filled_grid(TILE.COVERED)
            for y in range(self.height):
                for x in range(self.width):
                    if self._uncovered[y][x]:
                        output[y][x] = self._field[y][x]
                    if self._flagged[y][x]:
                        output[y][x] = TILE.FLAGGED
            self._field_cache = output
            return output
        else:
            return self._field_cache

    def _gen_filled_grid(self, value=0) -> List[List[int]]:
        field = []
        for _ in range(self.height):
            row = [value for _ in range(self.width)]
            field.append(row)
        return field

    def is_valid_tile(self, x, y) -> bool:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        return True

    def random_fill(self, mine_count: int):
        self.reset()
        for _ in range(mine_count):
            while True:
                rx = randint(0, self.width - 1)
                ry = randint(0, self.height - 1)
                if self._field[ry][rx] > 9:
                    continue
                self.set_mine(rx, ry)
                break

    def uncover(self, x, y) -> bool:
        if not self.is_valid_tile(x, y):
            return False
        if self._uncovered[y][x] or self._flagged[y][x]:
            return False

        self._uncovered[y][x] = 1
        flags_around = 0
        for ax in range(-1, 2):
            for ay in range(-1, 2):
                if ax == ay == 0:
                    continue
                if self.is_valid_tile(x, y) and self._flagged[y][x]:
                    flags_around += 1

        if self._field[y][x] == flags_around:
            for ax in range(-1, 2):
                for ay in range(-1, 2):
                    if ax == ay == 0:
                        continue
                    self.uncover(x + ax, y + ay)

        self._updated = True
        return True

    def reset(self):
        self.mine_count = 0
        self._flagged = self._gen_filled_grid()
        self._uncovered = self._gen_filled_grid()
        self._field = self._gen_filled_grid()
        self._updated = True

    def cover(self):
        self._flagged = self._gen_filled_grid()
        self._uncovered = self._gen_filled_grid()
        self._updated = True

    def cover_pos(self, x, y) -> bool:
        if not self.is_valid_tile(x, y):
            return False
        if not self._uncovered[y][x]:
            return False

        self._uncovered[y][x] = False
        self._updated = True
        return True

    def set_mine(self, x, y) -> bool:
        if not self.is_valid_tile(x, y):
            return False

        if self._field[y][x] > 9:
            return False

        self.mine_count += 1
        self._field[y][x] = 10

        for ax in range(-1, 2):
            for ay in range(-1, 2):
                if ax == ay == 0:
                    continue
                if self.is_valid_tile(x + ax, y + ay):
                    self._field[y + ay][x + ax] += 1

        self._updated = True

    def flag(self, x, y) -> bool:
        if not self.is_valid_tile(x, y):
            return False

        self._flagged[y][x] = not self._flagged[y][x]
        self._updated = True
