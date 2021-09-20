from Map import Map, TileState
from Player import Player
from Helpers import print_log


# --------------- init -------------- #
init_msg = input()
parsed = list(map(int, init_msg.split()[1:]))
player = Player(parsed[2], parsed[3], parsed[4], parsed[5], parsed[6], parsed[7], parsed[8])
game_map = Map(parsed[0], parsed[1], parsed[9])
maxBombRange, deadzoneStart, deadzoneDelay, maxStep = parsed[9:]
# height, width, x, y, health, bombRange, trapCount, vision, bombDelay, maxBombRange, deadzoneStart, deadzoneDelay, maxStep = map(int, init_msg.split()[1:])
print('init confirm')

while True:
    state_msg = input()
    if state_msg.startswith('term'):
        break
    # Do stuff
    if state_msg.split()[-1] == 'EOM':
        state_msg_list = list(map(int, state_msg.split()[:-1]))

        stepCount, lastActionTakenByThePlayer, x, y, health, healthUpgradeCount, bombRange, trapCount = state_msg_list[:8]
        player.update(lastActionTakenByThePlayer, x, y, health, healthUpgradeCount, bombRange, trapCount)

        if state_msg_list[8] == 1:
            other_x, other_y, other_health = state_msg_list[9:12]
            numberOfTilesInVision = state_msg_list[12]
            tileInfo = state_msg_list[13:]
        else:
            numberOfTilesInVision = state_msg_list[9]
            tileInfo = state_msg_list[10:]

        game_map.update(numberOfTilesInVision, tileInfo)
        
    
    def next_action():
        surroundings = player.get_surrounding_pos()
        tiles_states = game_map.get_surrounding_tiles(player.x , player.y)
        
        #check if player on bomb
        if game_map.tile_has_state(player.x , player.y, TileState.BOMB):
            for row,col in surroundings:
                if game_map.is_free_tile(row, col): # moves to first free tile. needs improvement
                    player.move_to(row, col)
                    return

        for dir,states in tiles_states:
            #check if next to other player
            if TileState.PLAYER in states:
                getattr(player, 'place_trap_'+dir)() #place trap on player??
                return
            #check if next to box
            if TileState.BOX in states:
                player.place_bomb()
                return

        
    player.random_action()
