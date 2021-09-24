from Map import Tile, Map, TileState
from Player import Player
from Helpers import print_log, dijkistra


# --------------- init -------------- #
init_msg = input()
parsed = list(map(int, init_msg.split()[1:]))
player = Player(parsed[2], parsed[3], parsed[4], parsed[5], parsed[6], parsed[7], parsed[8])
game_map = Map(parsed[0], parsed[1], parsed[9])
maxBombRange, deadzoneStart, deadzoneDelay, maxStep = parsed[9:]
# height, width, x, y, health, bombRange, trapCount, vision, bombDelay, maxBombRange, deadzoneStart, deadzoneDelay, maxStep = map(int, init_msg.split()[1:])
print('init confirm')


def next_action():
        surr_tiles = game_map.get_surrounding_tiles(player.x , player.y)
        
        #check if player on bomb
        if game_map.tile_has_state(player.x , player.y, TileState.BOMB):
            for dir,tile in surr_tiles.items():
                if tile.is_safe:
                    getattr(player, 'go_'+dir)()
                    return

        #check surrounding tiles
        for dir,tile in surr_tiles.items():
            #check if next to other player
            if tile.has_state(TileState.PLAYER):
                if player.trapCount > 0:
                    getattr(player, 'place_trap_'+dir)() #place trap on player
                else:
                    player.place_bomb()

            # check if next to deadzone
            # elif tile.has_state(TileState.DEADZONE):
            
            # check if next to box
            elif tile.has_state(TileState.BOX):
                player.place_bomb() # TODO: check if able to flee
            # check if next to safe upgrade
            elif tile.is_safe and\
                (tile.has_state(TileState.HEALTH_UPGRADE)\
                or tile.has_state(TileState.BOMB_UPGRADE)\
                or tile.has_state(TileState.TRAP_UPGRADE)):
                getattr(player, 'go_'+dir)()

            else: continue
            return


        for tile in game_map.vision:

            # in bomb fire range
            if tile.has_state(TileState.BOMB):
                if player.x == tile.row and abs(player.y-tile.col) <= maxBombRange:
                    if 'down' in surr_tiles and surr_tiles['down'].is_safe: player.go_down()
                    elif 'up' in surr_tiles and surr_tiles['up'].is_safe: player.go_up()
                elif player.y == tile.col and abs(player.x-tile.row) <= maxBombRange:
                    if 'right' in surr_tiles and surr_tiles['right'].is_safe: player.go_right()
                    elif 'left' in surr_tiles and surr_tiles['left'].is_safe: player.go_left()
                # else:
                    # move in fire direction to get out of corners??

            # #player in vision
            # elif other_x is not None:
            #     pass

            # move to box or upgrade in vision
            elif tile.has_state(TileState.BOX)\
                or tile.has_state(TileState.HEALTH_UPGRADE)\
                or tile.has_state(TileState.BOMB_UPGRADE)\
                or tile.has_state(TileState.TRAP_UPGRADE)\
                or tile.has_state(TileState.BOX_BROKEN):
                # TODO: find all boxes or upgrades and move to the one closest to the center
                path = dijkistra(game_map, game_map.tiles[player.x][player.y], tile)
                if path: player.move_to(path[0]) #???????
            
            else: continue
            return

        # just move towards center of map if found nothing
        path = dijkistra(game_map, game_map.tiles[player.x][player.y], game_map.center_tile())
        player.move_to(path[0]) if path else player.stay()

        # player.random_action()
                     

while True:
    state_msg = input()
    if state_msg.startswith('term'):
        break
    if state_msg.split()[-1] == 'EOM':
        state_msg_list = list(map(int, state_msg.split()[:-1]))

        stepCount, lastActionTakenByThePlayer, x, y, health, healthUpgradeCount, bombRange, trapCount = state_msg_list[:8]
        player.update(lastActionTakenByThePlayer, x, y, health, healthUpgradeCount, bombRange, trapCount)

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
