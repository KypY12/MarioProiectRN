from objects.tile import *
from objects.player import *
from objects.enemy import *
from objects.bonus import *
from objects.finish import *


def get_element_as_object(element, x, y):
    if element == " ":
        return None
    elif element == "T":
        return Tile(None, x*TILE_WIDTH, y*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
    elif element == "E":
        return Enemy(None, x*TILE_WIDTH, y*TILE_HEIGHT, 2*TILE_WIDTH, 2*TILE_HEIGHT)
    elif element == "B":
        return Bonus(None, x*TILE_WIDTH, y*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
    elif element == "P":
        return Player(None, x*TILE_WIDTH, y*TILE_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    elif element == "F":
        return Finish(None, x*TILE_WIDTH, y*TILE_HEIGHT, 2*TILE_WIDTH, 3*TILE_HEIGHT)


def get_objects_from_matrix_map(matrix_map):
    tiles = []
    enemies = []
    bonuses = []
    finish_states = []
    player = None

    for element_line, line in enumerate(matrix_map):
        for element_column, element in enumerate(line):
            obj = get_element_as_object(element, element_column, element_line)
            if obj is not None:
                if type(obj) == Enemy:
                    enemies.append(obj)
                elif type(obj) == Player:
                    player = obj
                elif type(obj) == Bonus:
                    bonuses.append(obj)
                elif type(obj) == Finish:
                    finish_states.append(obj)
                else:
                    tiles.append(obj)

    TILES_COUNT_X = len(matrix_map[0])
    TILES_COUNT_Y = len(matrix_map)
    WINDOW_HEIGHT = TILE_HEIGHT * TILES_COUNT_Y
    return TILES_COUNT_X, TILES_COUNT_Y, WINDOW_HEIGHT, tiles, player, enemies, bonuses, finish_states


def load_map(file_name):
    matrix_map = []
    with open(file_name, "r") as file:
        line = file.readline()
        while line:
            matrix_map.append(list(line.split("|~0")[0]))
            line = file.readline()

    return get_objects_from_matrix_map(matrix_map)
