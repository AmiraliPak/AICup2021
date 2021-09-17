from enum import Enum
from Helpers import print_log
import numpy as np

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
        self.tiles = np.array([[None for col in range(width)] for row in range(height)])
        #print_log(self.tiles)

    def tile_has_state(self, row, col, tile_state:TileState):
        return (self.tiles[row][col] >> tile_state.value) % 2 == 1

    def get_tile_states(self, row, col):
        states :list[TileState] = []
        state_num = self.tiles[row][col]
        index = 0
        while state_num != 0:
            if state_num % 2 == 1:
                states.append(TileState(index))
            state_num = state_num >> 1
            index += 1
        return states
    
    def update(self, tiles_count, tile_info):
        i = 0
        while i < 3 * tiles_count:
            row, col, val = tile_info[i:i+3]
            self.tiles[row][col] = val
            i += 3

    def log_tile_states(self, row:int, col:int):
        log = f'state({row},{col})=> '
        states = self.get_tile_states(row, col)
        log += ', '.join(map(lambda s: s.name, states))
        print_log(log)