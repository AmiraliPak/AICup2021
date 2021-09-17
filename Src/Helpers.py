import sys


def print_log(text:str): print(text, file=sys.stderr)

def manhattan_distance(self, row1, col1, row2, col2):
    distance = abs(row1 - row2) + abs(col1 - col2)
    return distance
