from enum import Enum
import numpy as np
import heapq, math


def manhattan_distance(tile1, tile2) -> int:
    distance = abs(tile1.row - tile2.row) + abs(tile1.col - tile2.col)
    return distance

def pi_edge(u, v, end_tile):
    return 1 + manhattan_distance(v,end_tile) - manhattan_distance(u,end_tile)

def dijkistra(game_map, start_tile, end_tile):
    if start_tile == end_tile: return []

    # tiles should be reset
    unprocessed = []
    start_tile.distance = 0
    push_order = 0
    heapq.heappush(unprocessed,(0, push_order, start_tile))
    push_order += 1
    tile = None
    max_loops = 1000
    counter = 0
    while len(unprocessed) != 0 and counter <= max_loops:
        _,_,tile = heapq.heappop(unprocessed)
        if tile.is_processed:
            continue
        tile.is_processed = True
        if tile == end_tile: return get_path(start_tile, end_tile)

        for neighbor in game_map.get_surrounding_tiles(tile.row, tile.col).values():
            if (neighbor == end_tile or neighbor.can_be_in_path()) and not neighbor.is_processed:
                new_dist = tile.distance + pi_edge(tile,neighbor,end_tile)
                if new_dist < neighbor.distance:
                    neighbor.distance = new_dist
                    neighbor.parent = tile
                    heapq.heappush(unprocessed,(new_dist, push_order, neighbor))
                    push_order += 1

    if tile is None or tile == start_tile:
        return []
    return get_path(start_tile, tile) 

def get_path(start_tile, end_tile):
    path = []
    tile = end_tile
    tile = tile.parent
    while tile != start_tile:
        path.append(tile)
        tile = tile.parent
    path.reverse()
    return path

def closest_tile(source_tile, tiles:list):
    closest_tile = None
    min_mandist = math.inf
    for tile in tiles:
        mandist = manhattan_distance(source_tile, tile)
        if mandist < min_mandist:
            min_mandist = mandist
            closest_tile = tile
    return closest_tile


class Action(Enum):
    GO_LEFT = 0
    GO_RIGHT = 1
    GO_UP = 2
    GO_DOWN = 3
    STAY = 4
    PLACE_BOMB = 5
    PLACE_TRAP_LEFT = 6
    PLACE_TRAP_RIGHT = 7
    PLACE_TRAP_UP = 8
    PLACE_TRAP_DOWN = 9
    INIT = 10
    NO_ACTION = 11


class Player:
    def __init__(self, x, y, health, bombRange, trapCount, vision, bombDelay):
        self.x = x
        self.y = y
        self.health = health
        self.bombRange = bombRange
        self.trapCount = trapCount
        # self.vision = vision
        self.bombDelay = bombDelay
        self.healthUpgradeCount = 0
        # self.lastAction:Action = None
        self.bomb_step_counter = 0

    # def update(self, lastAction, x, y, health, healthUpgradeCount, bombRange, trapCount):
    def update(self, x, y, health, healthUpgradeCount, bombRange, trapCount):
        # self.lastAction = Action(lastAction)
        self.x = x
        self.y = y
        self.health = health
        self.bombRange = bombRange
        self.trapCount = trapCount
        self.healthUpgradeCount = healthUpgradeCount
        if self.bomb_step_counter > 0: self.bomb_step_counter -= 2

    def go_left(self):          print(0)
    def go_right(self):         print(1)
    def go_up(self):            print(2)
    def go_down(self):          print(3)
    def stay(self):             print(4)
    def place_bomb(self):
        print(5)
        self.bomb_step_counter = self.bombDelay + 2
    def place_trap_left(self):  print(6)
    def place_trap_right(self): print(7)
    def place_trap_up(self):    print(8)
    def place_trap_down(self):  print(9)
    
    def move_to(self, tile):
        row, col = tile.row, tile.col
        '''Moves to an ADJACENT tile'''
        if row == self.x + 1 and col == self.y:
            self.go_down()
        elif row == self.x - 1 and col == self.y:
            self.go_up()
        elif row == self.x and col == self.y - 1:
            self.go_left()
        elif row == self.x and col == self.y + 1:
            self.go_right()


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

# --------------- init -------------- #
init_msg = input()
parsed = list(map(int, init_msg.split()[1:]))
player = Player(parsed[2], parsed[3], parsed[4], parsed[5], parsed[6], parsed[7], parsed[8])
game_map = Map(parsed[0], parsed[1], parsed[9], parsed[8], player)
maxBombRange, deadzoneStart, deadzoneDelay, maxStep = parsed[9:]
# height, width, x, y, health, bombRange, trapCount, vision, bombDelay, maxBombRange, deadzoneStart, deadzoneDelay, maxStep = map(int, init_msg.split()[1:])
print('init confirm')


def next_action():
        surr_tiles = game_map.get_surrounding_tiles(player.x , player.y)
        player_tile:Tile = game_map.tiles[player.x,player.y]
        
        #check if player on bomb or fire ------------------------------------------------------------------
        if player_tile.has_state(TileState.FIRE) or player_tile.has_state(TileState.BOMB):
            for dir,tile in surr_tiles.items():
                if tile.is_safe:
                    getattr(player, 'go_'+dir)()
                    return

        #check surrounding tiles
        for dir,tile in surr_tiles.items():
            #check if next to other player ------------------------------------------------------------------
            if tile.has_state(TileState.PLAYER):
                if player.trapCount > 0:
                    getattr(player, 'place_trap_'+dir)() #place trap on player
                elif player.bomb_step_counter == 0:
                    player.place_bomb()
                    player_tile.place_bomb()
                else: continue
                return

            # check if next to deadzone ------------------------------------------------------------------
            # elif tile.has_state(TileState.DEADZONE):
            
        in_bomb_range = None
        for tile in game_map.vision:
            # in bomb fire range and probably stuck ------------------------------------------------------------------
            if tile.has_state(TileState.BOMB):
                bomb_range = player.bombRange if tile.own_bomb else maxBombRange
                if player.x == tile.row and abs(player.y-tile.col) <= bomb_range:
                    in_bomb_range = 'row'
                    if (not 'down' in surr_tiles or not surr_tiles['down'].is_safe)\
                        and (not 'up' in surr_tiles or not surr_tiles['up'].is_safe):
                        if player.y>tile.col:
                            if 'right' in surr_tiles and surr_tiles['right'].is_safe: player.go_right()
                            elif 'left' in surr_tiles: player.go_left()
                            else: continue
                            return
                        elif player.y<tile.col:
                            if 'left' in surr_tiles and surr_tiles['left'].is_safe: player.go_left()
                            elif 'right' in surr_tiles: player.go_right()
                            else: continue
                            return
                elif player.y == tile.col and abs(player.x-tile.row) <= bomb_range:
                    in_bomb_range = 'col'
                    if (not 'left' in surr_tiles or not surr_tiles['left'].is_safe)\
                        and (not 'right' in surr_tiles or not surr_tiles['right'].is_safe):
                            if player.x>tile.row:
                                if 'down' in surr_tiles and surr_tiles['down'].is_safe: player.go_down()
                                elif 'up' in surr_tiles: player.go_up()
                                else: continue
                                return
                            elif player.x<tile.row:
                                if 'up' in surr_tiles and surr_tiles['up'].is_safe: player.go_up()
                                elif 'down' in surr_tiles: player.go_down()
                                else: continue
                                return

        for dir,tile in surr_tiles.items():
            # check if next to box ------------------------------------------------------------------
            if tile.has_state(TileState.BOX) and player.bomb_step_counter == 0:
                player.place_bomb() # TODO: check if able to flee
                game_map.tiles[player.x,player.y].place_bomb()
            # check if next to safe upgrade ------------------------------------------------------------------
            elif tile.is_safe and\
                (tile.has_state(TileState.HEALTH_UPGRADE)\
                or tile.has_state(TileState.BOMB_UPGRADE)\
                or tile.has_state(TileState.TRAP_UPGRADE)):
                getattr(player, 'go_'+dir)()
            else: continue
            return


        health_tiles = []
        upgrade_tiles = []
        box_tiles = []
        for tile in game_map.vision:
            # #player in vision ------------------------------------------------------------------
            # elif other_x is not None:
            #     pass

            # move to box or upgrade in vision ------------------------------------------------------------------
            if tile.has_state(TileState.HEALTH_UPGRADE): health_tiles.append(tile)
            elif tile.has_state(TileState.BOMB_UPGRADE) or tile.has_state(TileState.TRAP_UPGRADE): upgrade_tiles.append(tile)
            elif tile.has_state(TileState.BOX): box_tiles.append(tile)
            # if tile.has_state(TileState.BOX)\
            #     or tile.has_state(TileState.HEALTH_UPGRADE)\
            #     or tile.has_state(TileState.BOMB_UPGRADE)\
            #     or tile.has_state(TileState.TRAP_UPGRADE)\
            #     or tile.has_state(TileState.BOX_BROKEN):
            #     print_log('path find to box or upgrade')
            #     # TODO: find all boxes or upgrades and move to the one closest to the center or the important one
            #     path = dijkistra(game_map, game_map.tiles[player.x,player.y], tile)
            #     if path:
            #         player.move_to(path[0]) #???????
            #         print_log(f'move to ({path[0].row},{path[0].col})')
            #         return
        target_tile = None
        if health_tiles: target_tile = closest_tile(player_tile, health_tiles)
        elif upgrade_tiles: target_tile = closest_tile(player_tile, upgrade_tiles)
        elif box_tiles: target_tile = closest_tile(player_tile, box_tiles)
        if target_tile is not None:
            path = dijkistra(game_map, player_tile, target_tile)
            if path:
                player.move_to(path[0]) #???????
                return


        if in_bomb_range == 'row':
            if 'down' in surr_tiles and surr_tiles['down'].is_safe: player.go_down()
            elif 'up' in surr_tiles and surr_tiles['up'].is_safe: player.go_up()
        elif in_bomb_range == 'col':
            if 'left' in surr_tiles and surr_tiles['left'].is_safe: player.go_left()
            elif 'right' in surr_tiles and surr_tiles['right'].is_safe: player.go_right()
        else:
            # just move towards center of map if found nothing ------------------------------------------------------------------
            path = dijkistra(game_map, player_tile, game_map.center_tile())
            if path:
                player.move_to(path[0])
            else:
                player.stay()

        # player.random_action()
                     

while True:
    state_msg = input()
    if state_msg.startswith('term'):
        break
    if state_msg.split()[-1] == 'EOM':
        state_msg_list = list(map(int, state_msg.split()[:-1]))

        stepCount, lastActionTakenByThePlayer, x, y, health, healthUpgradeCount, bombRange, trapCount = state_msg_list[:8]
        # player.update(lastActionTakenByThePlayer, x, y, health, healthUpgradeCount, bombRange, trapCount)
        player.update(x, y, health, healthUpgradeCount, bombRange, trapCount)

        other_x, other_y, other_health = None, None, None
        if state_msg_list[8] == 1:
            other_x, other_y, other_health = state_msg_list[9:12]
            numberOfTilesInVision = state_msg_list[12]
            tileInfo = state_msg_list[13:]
        else:
            numberOfTilesInVision = state_msg_list[9]
            tileInfo = state_msg_list[10:]

        game_map.update(numberOfTilesInVision, tileInfo)
        # game_map.log_map()
        next_action()
        # player.random_action()
