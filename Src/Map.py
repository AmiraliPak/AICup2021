from enum import Enum
import math
import numpy as np
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
    TRAP = 9
    BOX_BROKEN = 10


class Tile:
    def __init__(self, row:int, col:int, state_val:int):
        self.states = []
        self.bomb_step_counter = 0
        self.own_bomb = False
        self.row = row
        self.col = col
        self.update(state_val)

    def update(self, state_val:int):
        self.is_new = True
        self.state_val = state_val
        self.update_states(state_val)
        self.set_is_safe()
        self.reset_node()

    def reset_node(self):
        self.distance = math.inf
        self.is_processed = False
        self.parent = None

    def update_states(self, state_val:int):
        # trap remains
        has_trap = self.has_state(TileState.TRAP)
        self.had_bomb = self.has_state(TileState.BOMB)
        self.states :list[TileState] = []
        if(has_trap): self.states.append(TileState.TRAP)

        index = 0
        while state_val != 0 and index <= 10:
            if state_val % 2 == 1:
                self.states.append(TileState(index))
            state_val = state_val >> 1
            index += 1

    def set_is_safe(self):
        if self.state_val == 0: # or len(self.states) == 0
            self.is_safe = True
            return
        # FREE_STATES = [TileState.BOMB_UPGRADE ,TileState.HEALTH_UPGRADE ,TileState.TRAP_UPGRADE] #maybe bomb
        UNSAFE_STATES = [TileState.DEADZONE, TileState.FIRE, TileState.BOX, TileState.WALL, TileState.BOMB, TileState.PLAYER, TileState.TRAP]
        self.is_safe = not any(item in UNSAFE_STATES for item in self.states)

    def set_on_fire(self):
        self.is_safe = False
        self.states.append(TileState.FIRE)

    def place_bomb(self): self.own_bomb = True

    def can_be_in_path(self):
        return self.is_safe or self.has_state(TileState.BOX) or self.has_state(TileState.PLAYER)

    def has_state(self, tile_state:TileState):
        return tile_state in self.states

    def __str__(self) -> str:
        return f'({self.row},{self.col},{self.state_val})'
    def __repr__(self) -> str:
        return f'({self.row},{self.col},{self.state_val})'


class Map:
    def __init__(self, height:int, width:int, maxBombRange, bombDelay, player):
        self.height = height
        self.width = width
        self.maxBombRange = maxBombRange
        self.player = player
        self.bombDelay = bombDelay
        # self.tiles = np.array([[None for col in range(width)] for row in range(height)])
        # self.tiles:list[list[Tile]] = [[None for col in range(width)] for row in range(height)]
        self.tiles = np.full((self.height,self.width), None, Tile)
        self.vision:list[Tile] = []

    def tile_has_state(self, row, col, tile_state:TileState): return self.tiles[row,col].has_state(tile_state)

    def get_tile_states(self, row, col): return self.tiles[row,col].states

    def tile_is_safe(self, row:int, col:int): return self.tiles[row,col].is_safe
    
    def update(self, tiles_count, tile_info:list[int]):
        self.vision = []
        bomb_tiles = []
        i = 0
        while i < 3 * tiles_count:
            row, col, val = tile_info[i:i+3]
            if self.tiles[row,col] is not None:
                self.tiles[row,col].update(val)
            else:
                self.tiles[row,col] = Tile(row, col, val)

            self.vision.append(self.tiles[row,col])
            # self.tiles[self.height - row -1,self.width - col -1] = val
            if self.tiles[row,col].has_state(TileState.BOMB):
                bomb_tiles.append(self.tiles[row,col])
            i += 3
        self.update_bomb_status(bomb_tiles)
        self.remove_old_tiles()

    def remove_old_tiles(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.tiles[i,j] is None: continue
                if self.tiles[i,j].is_new:
                    self.tiles[i,j].is_new = False
                else: self.tiles[i,j] = None

    def update_bomb_status(self, bomb_tiles:list[Tile]):
        for tile in bomb_tiles:
            if tile.had_bomb:
                tile.bomb_step_counter -= 2
                # if tile.bomb_step_counter == 2:
                #     self.explode_bomb(tile)
                if tile.bomb_step_counter == 0:
                    self.explode_bomb(tile)
                    tile.own_bomb = False
            else:
                if tile.own_bomb:
                    tile.bomb_step_counter = self.bombDelay - 2
                else:
                    tile.bomb_step_counter = self.bombDelay - 1
            print_log(f'({tile.row},{tile.col})=>bmbctr:{tile.bomb_step_counter}')

    def explode_bomb(self, bomb_tile:Tile):
        row, col = bomb_tile.row, bomb_tile.col
        bomb_range = self.player.bombRange if bomb_tile.own_bomb else self.maxBombRange
        # set row on fire
        col_start = max(col-bomb_range,0)
        col_end = min(col+bomb_range+1,self.width)
        for tile in self.tiles[row,col_start:col_end]:
            if tile is None: continue
            tile.set_on_fire()
        # set col on fire
        row_start = max(row-bomb_range,0)
        row_end = min(row+bomb_range+1,self.height)
        print_log(f'[{row_start}:{row_end},{col}] , {self.height}={len(self.tiles)} , {self.width}={len(self.tiles[0])}')
        for tile in self.tiles[row_start:row_end,col]:
            if tile is None: continue
            tile.set_on_fire()

    def center_tile(self): return Tile(self.height//2, self.width//2, 0)

    # def log_tile_states(self, row:int, col:int):
    #     log = f'state({row},{col})=> '
    #     states = self.tiles[row,col].states
    #     log += ', '.join(map(lambda s: s.name, states))
    #     print_log(log)

    def get_surrounding_tiles(self, row:int, col:int) -> dict[str,Tile]:
        tiles = {}
        if row > 0              and self.tiles[row-1,col  ] is not None: tiles['up']     = self.tiles[row-1,col  ]
        if row+1 < self.height  and self.tiles[row+1,col  ] is not None: tiles['down']   = self.tiles[row+1,col  ]
        if col > 0              and self.tiles[row  ,col-1] is not None: tiles['left']   = self.tiles[row  ,col-1]
        if col+1 < self.width   and self.tiles[row  ,col+1] is not None: tiles['right']  = self.tiles[row  ,col+1]
        return tiles

    # def log_map(self):
    #     for row in range(self.height):
    #         row_log = ''
    #         for col in range(self.width):
    #             row_log += str(self.tiles[row,col])+' '
    #         print_log(row_log)
