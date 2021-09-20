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
    TRAP = 9

class Map:
    def __init__(self, height:int, width:int, maxBombRange):
        self.height = height
        self.width = width
        self.maxBombRange = maxBombRange
        self.tiles = np.array([[None for col in range(width)] for row in range(height)])
        #print_log(self.tiles)

    def tile_has_state(self, row, col, tile_state:TileState):
        return (self.tiles[row][col] >> tile_state.value) % 2 == 1

    def get_tile_states(self, row, col):
        states :list[TileState] = []
        state_num = self.tiles[row][col]
        index = 0
        while state_num != 0 and index <= 9:
            if state_num % 2 == 1:
                states.append(TileState(index))
            state_num = state_num >> 1
            index += 1
        return states
    
    def update(self, tiles_count, tile_info):
        self.reset_map()
        i = 0
        while i < 3 * tiles_count:
            row, col, val = tile_info[i:i+3]
            self.tiles[row][col] = val
            self.tiles[self.height - row -1][self.width - col -1] = val
            i += 3
            # self.log_tile_states(row, col)

    def log_tile_states(self, row:int, col:int):
        log = f'state({row},{col})=> '
        states = self.get_tile_states(row, col)
        log += ', '.join(map(lambda s: s.name, states))
        print_log(log)

    def is_free_tile(self, row:int, col:int):
        if self.tiles[row][col] == 0:
            return True
        states = self.get_tile_states(row, col)
        FREE_STATES = [TileState.BOMB_UPGRADE ,TileState.HEALTH_UPGRADE ,TileState.TRAP_UPGRADE] #maybe bomb
        return any(item in FREE_STATES for item in states)

    def get_surrounding_tiles(self, row:int, col:int):
        tiles = {}
        tiles['up']    = self.get_tile_states(row-1, col  )
        tiles['down']  = self.get_tile_states(row+1, col  )
        tiles['left']  = self.get_tile_states(row  , col-1)
        tiles['right'] = self.get_tile_states(row  , col+1)
        return tiles

    def reset_map(self):
        #self.tiles = np.array([[None for col in range(self.width)] for row in range(self.height)])
        for col in range(self.width):
            for row in range(self.height):
                if self.tiles[col][row] != int(TileState.TRAP):
                    self.tiles[col][row] = None
        #self.tiles.fill(None)
    

    # def log_map(self):
    #     for row in range(self.height):
    #         for col in range(self.width):
    #             if self.tiles[row][col] is not None:
    #                 log_tile_states(row, col)