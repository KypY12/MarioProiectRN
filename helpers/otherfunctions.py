from globals import *
from objects.sensor import Sensor


def move_tiles(objects, scroll_movement):
    for object in objects:
        object.move(scroll_movement[0])


def draw_objects(objects, player):
    player.draw()
    for object in objects:
        object.draw()


def create_sensors(player, window):
    # y_unit = 2 * HEIGHT_SPACES_SIZE + SENSOR_HEIGHT
    # x_unit = 2 * WIDTH_SPACES_SIZE + SENSOR_WIDTH


    player_x = player.rect.x - SENSOR_PLAYER_OFFSET_X
    player_y = player.rect.y - SENSOR_PLAYER_OFFSET_Y

    sensors = []
    x_left = player_x
    x_right = x_left + 2*SENSOR_X_SPACE + player.rect.width
    y_up = player_y
    y_down = y_up + 2*SENSOR_Y_SPACE + player.rect.height
    # desenez fiecare patrat/dreptunghi
    for square_index in range(0, SENSOR_SQUARES_COUNT):
        x_diff = SENSOR_SQUARE_X_OFFSET
        y_diff = SENSOR_SQUARE_Y_OFFSET
        current_x = x_left
        current_y = y_up

        # linia de sus
        while current_x <= x_right:
            sensors.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
            current_x += SENSOR_WIDTH + SENSOR_BETWEEN_X_SPACE

        current_x = sensors[-1].rect.x
        # x_diff = x_right - current_x
        x_right = current_x
        current_y = sensors[-1].rect.y + SENSOR_HEIGHT + SENSOR_BETWEEN_Y_SPACE
        # linia din dreapta
        while current_y <= y_down:
            sensors.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
            current_y += SENSOR_HEIGHT + SENSOR_BETWEEN_Y_SPACE

        current_x = sensors[-1].rect.x - SENSOR_WIDTH - SENSOR_BETWEEN_X_SPACE
        current_y = sensors[-1].rect.y
        # y_diff = y_down - current_y
        y_down = current_y
        # linia de jos
        while current_x >= x_left:
            sensors.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
            current_x -= SENSOR_WIDTH + SENSOR_BETWEEN_X_SPACE

        current_x = sensors[-1].rect.x
        current_y = sensors[-1].rect.y - SENSOR_HEIGHT - SENSOR_BETWEEN_Y_SPACE
        up_limit = y_up + SENSOR_HEIGHT + SENSOR_BETWEEN_Y_SPACE
        # linia din stanga
        while current_y >= up_limit:
            sensors.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
            current_y -= SENSOR_HEIGHT + SENSOR_BETWEEN_Y_SPACE




        x_left -= 2 * SENSOR_X_SPACE - x_diff
        x_right += 2 * SENSOR_X_SPACE
        y_up -= 2 * SENSOR_Y_SPACE - y_diff
        y_down += 2 * SENSOR_Y_SPACE


    #
    # # Creez senzorii de sus
    #     for line_index in range(0, SENSOR_UP_LINES):
    #         line = []
    #         current_y = player_y - y_unit * (SENSOR_UP_LINES - line_index) + HEIGHT_SPACES_SIZE
    #         current_x = player_x - x_unit * SENSOR_LEFT_LINES + WIDTH_SPACES_SIZE
    #         line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
    #         for col_index in range(0, SENSOR_MATRIX_COLUMNS-1):
    #             current_x += x_unit
    #             line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
    #         sensors.append(line)
    #
    #     # Creez senzorii din stanga si din dreapta
    #     for line_index in range(0, PLAYER_HEIGHT_COUNT_SENSORS):
    #         line = []
    #         current_y = player_y + y_unit * line_index + HEIGHT_SPACES_SIZE
    #
    #         # stanga
    #         current_x = player_x - x_unit * SENSOR_LEFT_LINES + WIDTH_SPACES_SIZE
    #         line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
    #         for x in range(0, SENSOR_LEFT_LINES-1):
    #             current_x += x_unit
    #             line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
    #
    #         # dreapta
    #         current_x = player_x + player.rect.width + WIDTH_SPACES_SIZE
    #         line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
    #
    #         for x in range(0, SENSOR_RIGHT_LINES-1):
    #             current_x += x_unit
    #             line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
    #
    #         sensors.append(line)
    #
    #     # Creez senzorii de jos
    #     for line_index in range(0, SENSOR_DOWN_LINES):
    #         line = []
    #         current_y = player_y + player.rect.height + y_unit * line_index + HEIGHT_SPACES_SIZE
    #         current_x = player_x - x_unit * SENSOR_LEFT_LINES + WIDTH_SPACES_SIZE
    #         line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
    #         for col_index in range(0, SENSOR_MATRIX_COLUMNS - 1):
    #             current_x += x_unit
    #             line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
    #         sensors.append(line)
    #
    #
    #
    #     new_sensors = []
    #     for line in sensors:
    #         new_sensors += line
    #     sensors = new_sensors

    return sensors


def get_nn_input(sensors):
    input = []
    for sens in sensors:
        input += [sens.get_nn_input_value()]

    # print(np.array([input]))
    return input


def get_tile_map_position(x, first_tile_x):
    continuous_x = np.abs(x - first_tile_x)
    if continuous_x != 0:
        return int((continuous_x - (x % TILE_WIDTH))/TILE_WIDTH)
    else:
        return 0

# def draw_tiles(rects, scroll_move):
#     for rect in rects:
#         rect.draw(scroll_move)
#         # if type(rect) != Player:
#             # rect.x -= scroll_move[0]
#             # rect.y -= scroll_move[1]
#             # (player_coords[0] + scroll_move[0] - PLAYER_BACK_OFFSET)/20
#             # rect.y -= (player_coords[1] + scroll_move[1])/20
#             # pygame.draw.rect(window, (255, 255, 255), rect, 0)

#
# def move_and_draw_enemies(enemies, rects, scroll_move):
#     for enemy in enemies:
#         enemy.move(rects)
#         enemy.draw(scroll_move)




