from Map import Map
from Player import Player
import random
from Helpers import print_log



# --------------- init -------------- #
init_msg = input()
parsed = map(int, init_msg.split()[1:])
player = Player(parsed[2], parsed[3], parsed[4], parsed[5], parsed[6], parsed[7], parsed[8])
# maxBombRange, deadzoneStart, deadzoneDelay, maxStep = parsed[9:]
game_map = Map(parsed[0], parsed[1])
# height, width, x, y, health, bombRange, trapCount, vision, bombDelay, maxBombRange, deadzoneStart, deadzoneDelay, maxStep = map(int, init_msg.split()[1:])
# Do stuff
print('init confirm')

while True:
    state_msg = input()
    if 'term' in state_msg:
        break
    # Do stuff
    print(int(random.random() * 10))

