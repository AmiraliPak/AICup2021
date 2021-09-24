from enum import Enum
import random


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
        self.vision = vision
        self.bombDelay = bombDelay
        self.healthUpgradeCount = 0
        self.lastAction:Action = None

    def update(self, lastAction, x, y, health, healthUpgradeCount, bombRange, trapCount):
        self.lastAction = Action(lastAction)
        self.x = x
        self.y = y
        self.health = health
        self.bombRange = bombRange
        self.trapCount = trapCount
        self.healthUpgradeCount = healthUpgradeCount

    def go_left(self):          print(0)
    def go_right(self):         print(1)
    def go_up(self):            print(2)
    def go_down(self):          print(3)
    def stay(self):             print(4)
    def place_bomb(self):       print(5)
    def place_trap_left(self):  print(6)
    def place_trap_right(self): print(7)
    def place_trap_up(self):    print(8)
    def place_trap_down(self):  print(9)
    
    def random_action(self):    print(int(random.random() * 10))

    def get_surrounding_pos(self): return [(self.x-1, self.y), (self.x+1, self.y), (self.x, self.y-1), (self.x, self.y+1)]

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
