import pygame
import numpy as np

WITH_SENSORS = True
DRAW_SENSORS = True
IS_WINDOW_FOLLOW_Y = False
DRAW_ALL = True

HUMAN_PLAYER = False
TRAIN_NN = True

KEEP_HISTORY = False
Q_HISTORY = []

MAX_ITERATIONS_PER_EPISODE = 10000

MAX_COUNT_FOR_AUTOSAVE = 1000
SAVES_COUNTER = 0
TIME_STAMP = 0

USE_EXPERIENCE_REPLAY = True
EXPERIENCE_MAX_REPLAYS = 10
EXPERIENCE_BATCH_LEN = 5

NN_ITER_IN_STATE = 10

Q_REWARD_BONUS_HIT = 1
Q_REWARD_ENEMY_KILLED = 1
Q_REWARD_WIN = 2

Q_REWARD_JUMPING = 0
Q_REWARD_MOVING_RIGHT = 0
Q_REWARD_MOVING_LEFT = -0.01

Q_REWARD_ENEMY_HIT = -1
Q_REWARD_GAP_FALL = -1
Q_SAME_POSITION_REWARD = -0.1


LIMIT_WHEN_START_DRAWING = 0

TILE_HEIGHT = 20
TILE_WIDTH = 20
TILES_COUNT_X = 0
TILES_COUNT_Y = 0

SENSOR_WIDTH = 20
SENSOR_HEIGHT = 20


SENSOR_X_SPACE = 50
SENSOR_Y_SPACE = 40
SENSOR_BETWEEN_X_SPACE = 30
SENSOR_BETWEEN_Y_SPACE = 19
# SENSOR_BETWEEN_X_SPACE = TILE_WIDTH * 2
# SENSOR_BETWEEN_Y_SPACE = TILE_HEIGHT - 1
SENSOR_SQUARES_COUNT = 5

# SENSOR_UP_LINES = 5
# SENSOR_DOWN_LINES = 5
# SENSOR_LEFT_LINES = 5
# SENSOR_RIGHT_LINES = 5

SENSOR_SQUARE_X_OFFSET = 30
SENSOR_SQUARE_Y_OFFSET = 15
SENSOR_PLAYER_OFFSET_X = 40
SENSOR_PLAYER_OFFSET_Y = 40

SENSOR_MAX_DISTANCE_COL_CHECK = 450

PLAYER_HEIGHT = 3 * TILE_HEIGHT
PLAYER_WIDTH = 2 * TILE_WIDTH

# PLAYER_WIDTH_COUNT_SENSORS = 1
# PLAYER_HEIGHT_COUNT_SENSORS = 1
# WIDTH_SPACES_SIZE = 15
# HEIGHT_SPACES_SIZE = 20

# SENSOR_MATRIX_LINES = SENSOR_UP_LINES + PLAYER_HEIGHT_COUNT_SENSORS + SENSOR_DOWN_LINES
# SENSOR_MATRIX_COLUMNS = SENSOR_LEFT_LINES + PLAYER_WIDTH_COUNT_SENSORS + SENSOR_RIGHT_LINES


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = TILE_HEIGHT * TILES_COUNT_Y

MAP_HEIGHT = 0
MAP_WIDTH = 0

PLAYER_BACK_OFFSET = WINDOW_WIDTH / 2 - WINDOW_WIDTH / 10
PLAYER_UP_OFFSET = WINDOW_HEIGHT / 2


TICK_RATE = 100

PLAYER_MOVEMENT_SPEED = 5
# PLAYER_JUMP_POWER = 40
PLAYER_MOMENTUM_STEP = 0.6


ENEMY_MOVEMENT_SPEED = 20

GRAVITY = 15


