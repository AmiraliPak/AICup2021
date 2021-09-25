from Map import Tile, Map, TileState
from Player import Player
from Helpers import print_log, dijkistra, closest_tile


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
            print_log('player on bomb or fire')
            for dir,tile in surr_tiles.items():
                if tile.is_safe:
                    getattr(player, 'go_'+dir)()
                    print_log(f'go {dir}')
                    return

        #check surrounding tiles
        for dir,tile in surr_tiles.items():
            #check if next to other player ------------------------------------------------------------------
            if tile.has_state(TileState.PLAYER):
                print_log('nxt to player')
                if player.trapCount > 0:
                    getattr(player, 'place_trap_'+dir)() #place trap on player
                    print_log('place_trap_'+dir)
                elif player.bomb_step_counter == 0:
                    print_log('bmbctr 0 place bomb')
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
                        print_log('stuck with bomb in same row')
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
                            print_log('stuck with bomb in same col')
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
                print_log('next to box and bmbctr 0\nplace bomb')
                player.place_bomb() # TODO: check if able to flee
                game_map.tiles[player.x,player.y].place_bomb()
            # check if next to safe upgrade ------------------------------------------------------------------
            elif tile.is_safe and\
                (tile.has_state(TileState.HEALTH_UPGRADE)\
                or tile.has_state(TileState.BOMB_UPGRADE)\
                or tile.has_state(TileState.TRAP_UPGRADE)):
                getattr(player, 'go_'+dir)()
                print_log('nxt to upgrade\ngo {dir}')
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
        print_log('path find to box or upgrade')
        if health_tiles: target_tile = closest_tile(player_tile, health_tiles)
        elif upgrade_tiles: target_tile = closest_tile(player_tile, upgrade_tiles)
        elif box_tiles: target_tile = closest_tile(player_tile, box_tiles)
        if target_tile is not None:
            print_log('pathfind '+str(player_tile) + ' to ' + str(target_tile))
            path = dijkistra(game_map, player_tile, target_tile)
            print_log('path')
            print_log(path)
            if path:
                player.move_to(path[0]) #???????
                print_log(f'move to ({path[0].row},{path[0].col})')
                return


        if in_bomb_range == 'row':
            print_log('at end run from bomb row')
            if 'down' in surr_tiles and surr_tiles['down'].is_safe: player.go_down()
            elif 'up' in surr_tiles and surr_tiles['up'].is_safe: player.go_up()
        elif in_bomb_range == 'col':
            print_log('at end run from bomb col')
            if 'left' in surr_tiles and surr_tiles['left'].is_safe: player.go_left()
            elif 'right' in surr_tiles and surr_tiles['right'].is_safe: player.go_right()
        else:
            # just move towards center of map if found nothing ------------------------------------------------------------------
            path = dijkistra(game_map, player_tile, game_map.center_tile())
            if path:
                player.move_to(path[0])
                print_log(f'path to center. move to ({path[0].row},{path[0].col})')
            else:
                player.stay()
                print_log(f'no path to center. stay')

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
