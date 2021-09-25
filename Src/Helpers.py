import sys, heapq, math


def print_log(obj): print(obj, file=sys.stderr)

def manhattan_distance(tile1, tile2) -> int:
    distance = abs(tile1.row - tile2.row) + abs(tile1.col - tile2.col)
    return distance

def pi_edge(u, v, end_tile):
    return 1 + manhattan_distance(v,end_tile) - manhattan_distance(u,end_tile)

def dijkistra(game_map, start_tile, end_tile):
    print_log('start' + str(start_tile))
    print_log('end' + str(end_tile))
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
