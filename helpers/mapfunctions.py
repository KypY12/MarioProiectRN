from objects.tile import *
from objects.player import *
from objects.enemy import *
from objects.bonus import *
from objects.finish import *

import globals

import numpy as np


def get_element_as_object(element, x, y, window):
    if element == " ":
        return None
    elif element == "T":
        return Tile(window, x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
    elif element == "E":
        return Enemy(window, x * TILE_WIDTH, y * TILE_HEIGHT, 2 * TILE_WIDTH, 2 * TILE_HEIGHT)
    elif element == "B":
        return Bonus(window, x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
    elif element == "P":
        return Player(window, x * TILE_WIDTH, y * TILE_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    elif element == "F":
        return Finish(window, x * TILE_WIDTH, y * TILE_HEIGHT, 2 * TILE_WIDTH, 3 * TILE_HEIGHT)

    return None


def get_objects_from_matrix_map(matrix_map, window):
    tiles = []
    tiles_matrix = []
    enemies = []
    bonuses = []
    finish_states = []
    player = None
    first_obj = 0

    for element_line, line in enumerate(matrix_map):
        tiles_matrix_line = []
        for element_column, element in enumerate(line):
            obj = get_element_as_object(element, element_column, element_line, window)
            if obj is not None:
                if type(obj) == Enemy:
                    enemies.append(obj)
                    tiles_matrix_line.append("_")
                elif type(obj) == Player:
                    player = obj
                    tiles_matrix_line.append("_")
                elif type(obj) == Bonus:
                    bonuses.append(obj)
                    tiles_matrix_line.append("_")
                elif type(obj) == Finish:
                    finish_states.append(obj)
                    tiles_matrix_line.append("_")
                else:
                    tiles.append(obj)
                    tiles_matrix_line.append(obj)

                if element_column == 0:
                    first_obj = obj
            else:
                tiles_matrix_line.append("_")

        tiles_matrix.append(tiles_matrix_line)

    tiles_matrix = np.array(tiles_matrix).transpose()
    print(tiles_matrix.shape)
    tiles_matrix = [[x for x in y if x != "_"] for y in tiles_matrix]

    globals.TILES_COUNT_X = len(matrix_map[0])
    globals.TILES_COUNT_Y = len(matrix_map)
    globals.WINDOW_HEIGHT = globals.TILE_HEIGHT * globals.TILES_COUNT_Y
    return tiles, tiles_matrix, player, enemies, bonuses, finish_states, first_obj


def get_map_from_file(file_name):
    matrix_map = []
    with open(file_name, "r") as file:
        line = file.readline()
        while line:
            matrix_map.append(list(line.split("|~0")[0]))
            line = file.readline()
    return matrix_map


def load_map(file_name, window):
    return get_objects_from_matrix_map(get_map_from_file(file_name), window)


def set_map_params(file_name):
    matrix_map = get_map_from_file(file_name)
    globals.TILES_COUNT_X = len(matrix_map[0])
    globals.TILES_COUNT_Y = len(matrix_map)
    globals.WINDOW_HEIGHT = globals.TILE_HEIGHT * globals.TILES_COUNT_Y
    return globals.TILES_COUNT_X, globals.TILES_COUNT_Y, globals.WINDOW_HEIGHT

