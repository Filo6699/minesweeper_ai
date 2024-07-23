from typing import List, Tuple
from minesweeper import TILE


field = None
w, h = None, None
calculated = []


class ACTION:
    UNCOVER = 1
    FLAG = 2


class Move:
    def __init__(self, x: int, y: int, action: ACTION):
        self.x = x
        self.y = y
        self.action = action
        self.pos = [x, y]

    def __str__(self) -> str:
        return f"{self.pos} {self.action}"


class Tile:
    def __init__(self, x: int, y: int, value: int):
        self.x = x
        self.y = y
        self.value = value
        self.pos = [x, y]


class GroupInfo:
    def __init__(self, covered_cells: int, flags: int, mine_count: int):
        self.covered_cells = covered_cells
        self.flags = flags
        self.cells: Set[Tile] = set()
        self.covered_cells_set: Set[Tuple[int]] = set()
        self.mine_count: int = mine_count

    def __str__(self) -> str:
        return f"{self.covered_cells}/{len(self.cells)}  flags: {self.flags}  covered cells: {self.covered_cells_set}"


def get_cell(x, y):
    if x < 0 or y < 0 or x >= w or y >= h:
        return None
    return field[y][x]


def get_group_info(x, y) -> GroupInfo:
    value = get_cell(x, y)
    info = GroupInfo(0, 0, value)
    for ax in range(-1, 2):
        for ay in range(-1, 2):
            if ax == ay == 0:
                continue
            c = get_cell(x + ax, y + ay)
            if c == None:
                continue
            info.cells.add(Tile(x + ax, y + ay, c))
            if c == -1:
                info.covered_cells += 1
                info.covered_cells_set.add((x + ax, y + ay))
            elif c == -2 or c > 9:
                info.flags += 1
    return info


def calculate() -> List[Move]:
    global field, calculated

    groups: List[GroupInfo] = []
    moves: List[Move] = []

    def add_move(move: Move):
        if calculated[move.y][move.x]:
            return
        moves.append(move)
        if move.action == ACTION.FLAG:
            field[move.y][move.x] = -2
        calculated[move.y][move.x] = True

    tile_groups = []
    for _ in range(h):
        row = [[] for _ in range(w)]
        tile_groups.append(row)

    def process_groups(group_id1: int, group_id2: int):
        ccs1 = groups[group_id1].covered_cells_set
        ccs2 = groups[group_id2].covered_cells_set
        diff1 = ccs1.difference(ccs2)
        diff2 = ccs2.difference(ccs1)
        inter = ccs1.intersection(ccs2)
        inter_mines = max(
            groups[group_id1].mine_count - groups[group_id1].flags - len(diff1),
            groups[group_id2].mine_count - groups[group_id2].flags - len(diff2),
            0,
        )
        if len(diff1) == 0:
            inter_mines = groups[group_id1].mine_count - groups[group_id1].flags
            on_new_area = groups[group_id2].mine_count - groups[group_id2].flags - inter_mines
            if on_new_area == len(diff2):
                for tile in diff2:
                    add_move(Move(*tile, ACTION.FLAG))
            if on_new_area == 0:
                for tile in diff2:
                    add_move(Move(*tile, ACTION.UNCOVER))
        if len(diff2) == 0:
            inter_mines = groups[group_id2].mine_count - groups[group_id2].flags
            on_new_area = groups[group_id1].mine_count - groups[group_id1].flags - inter_mines
            if on_new_area == len(diff1):
                for tile in diff1:
                    add_move(Move(*tile, ACTION.FLAG))
            if on_new_area == 0:
                for tile in diff1:
                    add_move(Move(*tile, ACTION.UNCOVER))
        if inter_mines == 0:
            return
        if groups[group_id1].mine_count - groups[group_id1].flags == inter_mines:
            for tile in diff1:
                add_move(Move(*tile, ACTION.UNCOVER))
        if inter_mines == len(inter):
            for tile in inter:
                add_move(Move(*tile, ACTION.FLAG))
        if groups[group_id2].mine_count - groups[group_id2].flags == inter_mines:
            for tile in diff2:
                add_move(Move(*tile, ACTION.UNCOVER))

    for y in range(h):
        for x in range(w):
            value = field[y][x]
            if value < 1:
                continue
            info = get_group_info(x, y)

            if info.covered_cells + info.flags == value:
                for cell in info.covered_cells_set:
                    add_move(Move(*cell, ACTION.FLAG))
                    # if calculated[cell[1]][cell[0]]:
                    #     continue
                    # moves.append(Move(*cell, ACTION.FLAG))
                    # field[cell[1]][cell[0]] = -2
                    # calculated[cell[1]][cell[0]] = True
                continue

            if value - info.flags == 0:
                for cell in info.covered_cells_set:
                    add_move(Move(*cell, ACTION.UNCOVER))
                    # if calculated[cell[1]][cell[0]]:
                    #     continue
                    # moves.append(Move(*cell, ACTION.UNCOVER))
                    # calculated[cell[1]][cell[0]] = True
                continue

            cur_group_id = len(groups)
            groups.append(info)
            for tile in info.covered_cells_set:
                tile_groups[tile[1]][tile[0]].append(cur_group_id)

            for tile in info.covered_cells_set:
                for group_id in tile_groups[tile[1]][tile[0]]:
                    if group_id != cur_group_id:
                        process_groups(group_id, cur_group_id)

    return moves


def process_field(
    rfield: List[List[int]],
    width: int,
    height: int,
) -> List[Move]:
    global field, w, h, calculated
    field = rfield
    w, h = width, height

    calculated = []
    for _ in range(h):
        row = [False for _ in range(w)]
        calculated.append(row)

    moves: List[Move] = [
        *calculate(),
    ]

    return moves
