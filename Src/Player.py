from enum import Enum


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


class Player:
    def __init__(self, x, y, health, bombRange, trapCount, vision, bombDelay):
        self.x = x
        self.y = y
        self.health = health
        self.bombRange = bombRange
        self.trapCount = trapCount
        self.vision = vision
        self.bombDelay = bombDelay

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
