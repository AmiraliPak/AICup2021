from Map import Map
from Player import Player
import random
from Helpers import print_log



# --------------- init -------------- #
init_msg = input()
parsed = list(map(int, init_msg.split()[1:]))
player = Player(parsed[2], parsed[3], parsed[4], parsed[5], parsed[6], parsed[7], parsed[8])
game_map = Map(parsed[0], parsed[1])
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
            tileInfo = state_msg_list[12 : ]
        else:
            numberOfTilesInVision = state_msg_list[9]
            tileInfo = state_msg_list[9:]

        game_map.update(numberOfTilesInVision, tileInfo)
        # tiles_info = []
        # counter = 0
        # for tile in range(numberOfTilesInVision):
        #     tiles_info.append((tileInfo[tile + counter], tileInfo[tile + counter + 1], tileInfo[tile + counter + 2]))
        #     counter += 2
    
    def next_action():
        pass
        
    print(int(random.random() * 10))

