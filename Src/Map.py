from enum import Enum
import math
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
        self.update(row, col, state_val)

    def update(self, row:int, col:int, state_val:int):
        self.row = row
        self.col = col
        self.state_val = state_val
        self.set_states(state_val)
        self.set_is_safe()
        self.set_can_be_in_path()
        self.reset_node()

    def reset_node(self):
        self.distance = math.inf
        self.is_processed = False
        self.parent = None

    def set_states(self, state_val:int):
        # trap remains
        has_trap = self.has_state(TileState.TRAP)
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

    def set_can_be_in_path(self):
        self.can_be_in_path = self.is_safe or self.has_state(TileState.BOX) or self.has_state(TileState.PLAYER)

    def has_state(self, tile_state:TileState):
        return tile_state in self.states

    def __str__(self):
        return str(self.state_val)
    def __repr__(self):
        return str(self.state_val)


class Map:
    def __init__(self, height:int, width:int, maxBombRange):
        self.height = height
        self.width = width
        self.maxBombRange = maxBombRange
        # self.tiles = np.array([[None for col in range(width)] for row in range(height)])
        self.tiles:list[list[Tile]] = [[None for col in range(width)] for row in range(height)]
        self.vision:list[list[Tile]] = []

    def tile_has_state(self, row, col, tile_state:TileState): return self.tiles[row][col].has_state(tile_state)

    def get_tile_states(self, row, col): return self.tiles[row][col].states

    def tile_is_safe(self, row:int, col:int): return self.tiles[row][col].is_safe
    
    def update(self, tiles_count, tile_info:list[int]):
        self.vision = []
        i = 0
        while i < 3 * tiles_count:
            row, col, val = tile_info[i:i+3]
            if self.tiles[row][col] is not None:
                self.tiles[row][col].update(row, col, val)
            else:
                self.tiles[row][col] = Tile(row, col, val)

            self.vision.append(self.tiles[row][col])
            # self.tiles[self.height - row -1][self.width - col -1] = val
            i += 3

    def center_tile(self):
        return self.tiles[self.height/2][self.width/2]

    def log_tile_states(self, row:int, col:int):
        log = f'state({row},{col})=> '
        states = self.tiles[row][col].states
        log += ', '.join(map(lambda s: s.name, states))
        print_log(log)

    def get_surrounding_tiles(self, row:int, col:int) -> dict[str,Tile]:
        tiles = {}
        if row > 0:             tiles['up']     = self.tiles[row-1][col  ]
        if row+1 < self.height: tiles['down']   = self.tiles[row+1][col  ]
        if col > 0:             tiles['left']   = self.tiles[row  ][col-1]
        if col+1 < self.width:  tiles['right']  = self.tiles[row  ][col+1]
        return tiles

    def log_map(self):
        for row in range(self.height):
            row_log = ''
            for col in range(self.width):
                row_log += str(self.tiles[row][col])+' '
            print_log(row_log)