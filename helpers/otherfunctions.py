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
    y_unit = 2 * HEIGHT_SPACES_SIZE + SENSOR_HEIGHT
    x_unit = 2 * WIDTH_SPACES_SIZE + SENSOR_WIDTH

    sensors = []

    # Creez senzorii de sus
    for line_index in range(0, SENSOR_UP_LINES):
        line = []
        current_y = player.rect.y - y_unit * (SENSOR_UP_LINES - line_index) + HEIGHT_SPACES_SIZE
        current_x = player.rect.x - x_unit * SENSOR_LEFT_LINES + WIDTH_SPACES_SIZE
        line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
        for col_index in range(0, SENSOR_MATRIX_COLUMNS-1):
            current_x += x_unit
            line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
        sensors.append(line)

    # Creez senzorii din stanga si din dreapta
    for line_index in range(0, PLAYER_HEIGHT_COUNT_SENSORS):
        line = []
        current_y = player.rect.y + y_unit * line_index + HEIGHT_SPACES_SIZE

        # stanga
        current_x = player.rect.x - x_unit * SENSOR_LEFT_LINES + WIDTH_SPACES_SIZE
        line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
        for x in range(0, SENSOR_LEFT_LINES-1):
            current_x += x_unit
            line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))

        # dreapta
        current_x = player.rect.x + player.rect.width + WIDTH_SPACES_SIZE
        line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))

        for x in range(0, SENSOR_RIGHT_LINES-1):
            current_x += x_unit
            line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))

        sensors.append(line)

    # Creez senzorii de jos
    for line_index in range(0, SENSOR_DOWN_LINES):
        line = []
        current_y = player.rect.y + player.rect.height + y_unit * line_index + HEIGHT_SPACES_SIZE
        current_x = player.rect.x - x_unit * SENSOR_LEFT_LINES + WIDTH_SPACES_SIZE
        line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
        for col_index in range(0, SENSOR_MATRIX_COLUMNS - 1):
            current_x += x_unit
            line.append(Sensor(window, current_x, current_y, SENSOR_WIDTH, SENSOR_HEIGHT))
        sensors.append(line)





    new_sensors = []
    for line in sensors:
        new_sensors += line
    sensors = new_sensors

    return sensors


def get_nn_input(sensors):
    input = []
    for sens in sensors:
        input += [sens.get_nn_input_value()]

    # print(np.array([input]))
    return np.array([input])





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
