from enum import Enum
from Helpers import print_log


class TileState(Enum):
    DEADZONE = 0
    FIRE = 1
    BOX = 2
    WALL = 3
    BOMB = 4
    BOMB_UPGRADE = 5
    HEALTH_UPGRADE = 6
    TRAP_UPGRADE = 7
    PLAYER = 8


class Map:
    def __init__(self, height:int, width:int):
        self.height = height
        self.width = width
        self.tiles: list[list[str]] = [[None for col in range(width)] for row in range(height)]

    def tile_has_state(self, row, col, tile_state:TileState):
        return self.tiles[row][col][tile_state.value] == '1'

    def get_tile_states(self, row, col):
        states :list[TileState] = []
        for index,char in enumerate(self.tiles[row][col]):
            if char == '1':
                states.append(TileState(index))
        return states

    def log_tile_states(self, row:int, col:int):
        log = f'state({row},{col})=> '
        states = self.get_tile_states(row, col)
        log += ', '.join(map(lambda s: s.name, states))
        print_log(log)