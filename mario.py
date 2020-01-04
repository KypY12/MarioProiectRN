import random
import sys
import time

import pygame.locals


from helpers.mapfunctions import *
from helpers.mapgenerator import *
from helpers.otherfunctions import *
from objects.sensor import Sensor
from neural_network import *
import neural_network as nn
import globals


def gg_wp(window, score, count_iter):
    if count_iter > LIMIT_WHEN_START_DRAWING and globals.DRAW_ALL:
        font_1 = pygame.font.Font('freesansbold.ttf', 64)
        font_2 = pygame.font.Font('freesansbold.ttf', 32)

        game_over_text = font_1.render('GG WP', True, (0, 255, 0))
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
        window.blit(game_over_text, game_over_text_rect)

        score_text = font_2.render("Score : " + str(score), True, (0, 255, 0))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)
        window.blit(score_text, score_text_rect)

        pygame.display.flip()


def game_over(window, score, count_iter):
    if count_iter > LIMIT_WHEN_START_DRAWING and globals.DRAW_ALL:
        font_1 = pygame.font.Font('freesansbold.ttf', 64)
        font_2 = pygame.font.Font('freesansbold.ttf', 32)

        game_over_text = font_1.render('Game over', True, (255, 0, 0))
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
        window.blit(game_over_text, game_over_text_rect)

        score_text = font_2.render("Score : " + str(score), True, (255, 0, 0))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)
        window.blit(score_text, score_text_rect)

        pygame.display.flip()


def get_closer_objects_to(to_obj, first_obj, map_width_as_tile_pos, tiles_matrix, all_except_tiles):
    if to_obj in all_except_tiles:
        all_except_tiles.remove(to_obj)

    to_obj_tile_map_pos = get_tile_map_position(to_obj.rect.x, first_obj.rect.x)
    first_closer_pos = to_obj_tile_map_pos - map_width_as_tile_pos
    if first_closer_pos < 0:
        first_closer_pos = 0
    tile_list = tiles_matrix[first_closer_pos:to_obj_tile_map_pos + map_width_as_tile_pos]

    closer_objects = [x for y in tile_list for x in y]
    for obj in all_except_tiles:
        if abs(to_obj.rect.x - obj.rect.x) <= WINDOW_WIDTH:
            closer_objects.append(obj)

    return closer_objects


def get_much_closer_objects(closer_to_obj, obj):
    much_closer_objects = []
    for obj in closer_to_obj:
        if abs(obj.rect.x - obj.rect.x) <= SENSOR_MAX_DISTANCE_COL_CHECK:
            much_closer_objects.append(obj)
    return much_closer_objects


def apply_scroll_params(scroll_params, tiles, bonuses, finish_states, sensors, closer_to_obj, obj):
    for tile in tiles:
        tile.move(scroll_params)

    for bonus in bonuses:
        bonus.move(scroll_params)

    for finish in finish_states:
        finish.move(scroll_params)

    if globals.WITH_SENSORS:
        much_closer_objects = get_much_closer_objects(closer_to_obj, obj)
        for sensor in sensors:
            sensor.move(scroll_params, much_closer_objects)


def start_game(count_iter, count_to_autosave, window, clock):

    tiles, tiles_matrix, player, enemies, bonuses, finish_states, first_obj = load_map("maps/my_second_map.map", window)

    scroll_params = [0, 0]

    sensors = []
    if WITH_SENSORS:
        sensors = create_sensors(player, window)
        print("Count sensors: ", len(sensors))

    all_except_tiles = enemies + bonuses + finish_states

    count_iteration = 0
    state = []
    ai_pressed, previous_input, previous_output = [], [], []
    reward = 0
    count_same_position = 0
    map_width_as_tile_pos = get_tile_map_position(WINDOW_WIDTH, 0)

    experiences_for_replay = []

    # START GAME LOOP ==================================================================================================

    while True:
        # ===========================================================================================

        # ===========================================================================================
        # INITIAL
        # ===========================================================================================

        # Verific evenimente
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if pressed[pygame.K_SPACE]:
            globals.DRAW_ALL = False
            pygame.display.flip()
        elif pressed[pygame.K_d]:
            globals.DRAW_ALL = True
            pygame.display.flip()

        if pressed[pygame.K_t]:
            globals.TRAIN_NN = True
        elif pressed[pygame.K_y]:
            globals.TRAIN_NN = False

        # Verific daca e momentul pentru autosave
        if not HUMAN_PLAYER and count_to_autosave >= 500:
            nn.model.save("model.h5")
            count_to_autosave = 0
        count_to_autosave += 1

        # Punem in istoric valorile Q (daca KEEP_HISTORY este True)
        if not HUMAN_PLAYER and KEEP_HISTORY and len(globals.Q_HISTORY) >= 256:
            with open("q_history.txt", "a") as file:
                for q_list in globals.Q_HISTORY:
                    for q_elem in q_list:
                        file.write(str(q_elem) + "  ")
                    file.write("\n")
            globals.Q_HISTORY = []

        # ===========================================================================================

        # ===========================================================================================
        # RUN GAME ITERATION
        # ===========================================================================================

        if count_iter > LIMIT_WHEN_START_DRAWING and globals.DRAW_ALL:
            window.fill((0, 0, 0))

        # Se continua iteratia jocului

        closer_to_player_objects = get_closer_objects_to(player, first_obj, map_width_as_tile_pos, tiles_matrix, all_except_tiles)
        scroll_params, collide_enemy, collide_bonus, killed_enemies, is_win = player.move(ai_pressed, pressed,
                                                                                          closer_to_player_objects)

        # Daca a cazut in prapastie
        if player.rect.y > WINDOW_HEIGHT:
            reward += Q_REWARD_GAP_FALL
            game_over(window, player.score, count_iter)
            break

        # Daca s-a lovit de un inamic => Game Over
        if collide_enemy == "game_over":
            reward += Q_REWARD_ENEMY_HIT
            game_over(window, player.score, count_iter)
            break

        # Timp maxim pe episod
        if not HUMAN_PLAYER and count_iter == MAX_ITERATIONS_PER_EPISODE:
            reward += Q_REWARD_GAP_FALL
            game_over(window, player.score, count_iter)
            break

        # Daca sta mai mult pe loc schimbam rewardul sau chiar dam game_over
        if not HUMAN_PLAYER and scroll_params[0] == 0:
            count_same_position += 1
            if count_same_position >= 150:
                reward += Q_REWARD_GAP_FALL
                game_over(window, player.score, count_iter)
                break
            elif count_same_position % 10 == 0:
                reward += Q_SAME_POSITION_REWARD
        else:
            count_same_position = 0

        # Misc inamicii sa vad daca au lovit playerul
        # Daca playerul se misca si loveste el un inamic verific mai sus in player.move
        # Aici jos verific daca inamicul prin miscarea lui a lovit playerul
        # (De ex daca playerul sta pe loc dar inamicul se misca si il loveste, se verifica aici)
        enemy_hit = False
        for enemy in enemies:
            if enemy.move(player, tiles_matrix, first_obj, scroll_params):
                enemy_hit = True
                break
        if enemy_hit:
            reward += Q_REWARD_ENEMY_HIT
            game_over(window, player.score, count_iter)
            break

        # Daca a lovit finish dar nu a lovit in acelasi timp si un inamic => GG WP
        if is_win:
            reward += Q_REWARD_WIN
            gg_wp(window, player.score, count_iter)
            break

        # Distrugem toti inamicii ucisi (pot fi mai multi)
        for killed in killed_enemies:
            if killed in enemies:
                # reward atunci cand omoara un inamic
                reward += Q_REWARD_ENEMY_KILLED

                enemies.remove(killed)
                all_except_tiles.remove(killed)

        # Distrugem bonusurile pe care le-a atins playerul in iteratia curenta
        for bonus in collide_bonus:
            if bonus in bonuses:
                # reward atunci cand ia un bonus
                reward += Q_REWARD_BONUS_HIT

                bonuses.remove(bonus)
                all_except_tiles.remove(bonus)

        # Miscam dupa camera obiectele statice - Tile, Bonus, Finish, Sensor(daca e cazul)
        apply_scroll_params(scroll_params, tiles, bonuses, finish_states, sensors, closer_to_player_objects, player)

        # ===========================================================================================

        # ===========================================================================================
        # NEURAL NETWORK ACTIVITY
        # ===========================================================================================

        # Pentru NN
        state += get_nn_input(sensors)
        count_iteration += 1

        if not HUMAN_PLAYER and count_iteration == NN_ITER_IN_STATE:
            count_iteration = 0

            if TRAIN_NN and len(previous_input) > 0:
                if globals.USE_EXPERIENCE_REPLAY:
                    current_experience = [np.array([state]), reward, previous_input, previous_output]
                    if len(experiences_for_replay) < EXPERIENCE_MAX_REPLAYS:
                        experiences_for_replay.append(current_experience)
                    else:
                        experiences_for_replay = experiences_for_replay[1:] + [current_experience]
                        selected_batch = random.choices(experiences_for_replay, k=EXPERIENCE_BATCH_LEN)
                        train_network_batch(selected_batch)
                else:
                    train_network(np.array([state]), reward, previous_input, previous_output)

            # Preiau de la RN actiunea pe care o voi executa
            reward = 0
            ai_pressed, previous_input, previous_output = get_action_from_nn(np.array([state]))
            if ai_pressed == pygame.K_LEFT:
                reward += Q_REWARD_MOVING_LEFT * NN_ITER_IN_STATE
            elif ai_pressed == pygame.K_RIGHT:
                reward += Q_REWARD_MOVING_RIGHT * NN_ITER_IN_STATE
            state = []

        # ===========================================================================================

        # ===========================================================================================
        # DRAW CURRENT ITERATION
        # ===========================================================================================

        if globals.WITH_SENSORS and globals.DRAW_SENSORS:
            closer_to_player_objects += sensors

        count_iter += 1
        # Daca sa desenam sau nu imaginea jocului
        if count_iter > LIMIT_WHEN_START_DRAWING and globals.DRAW_ALL:
            draw_objects(closer_to_player_objects, player)
            pygame.display.flip()
            clock.tick(TICK_RATE)

        # END GAME LOOP ================================================================================================

    # Pentru NN
    if not HUMAN_PLAYER and count_iteration <= NN_ITER_IN_STATE:
        closer_objects = get_closer_objects_to(player, first_obj, map_width_as_tile_pos, tiles_matrix, all_except_tiles)
        much_closer_objects = much_closer_objects = get_much_closer_objects(closer_to_player_objects, player)

        for sensor in sensors:
            sensor.move(scroll_params, much_closer_objects)

        state += get_nn_input(sensors)

    if not HUMAN_PLAYER:
        # Prelucram putin
        missiong_count = int((NN_ITER_IN_STATE * len(sensors) - len(state)) / len(sensors))
        processed_state = state + state[len(state) - len(sensors):] * missiong_count

        if TRAIN_NN and len(previous_input) > 0:
            if globals.USE_EXPERIENCE_REPLAY:
                current_experience = [np.array([processed_state]), reward, previous_input, previous_output]
                if len(experiences_for_replay) < EXPERIENCE_MAX_REPLAYS:
                    experiences_for_replay.append(current_experience)
                else:
                    experiences_for_replay = experiences_for_replay[1:] + [current_experience]
                    selected_batch = random.choices(experiences_for_replay, k=EXPERIENCE_BATCH_LEN)
                    train_network_batch(selected_batch)
            else:
                train_network(np.array([processed_state]), reward, previous_input, previous_output)

        # Punem in istoric valorile Q (daca KEEP_HISTORY este True)
        if KEEP_HISTORY:
            with open("q_history.txt", "a") as file:
                for q_list in globals.Q_HISTORY:
                    for q_elem in q_list:
                        file.write(str(q_elem) + "  ")
                    file.write("\n")
                globals.Q_HISTORY = []

    if HUMAN_PLAYER:
        time.sleep(2)

    return True


pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

TILES_COUNT_X, TILES_COUNT_Y, WINDOW_HEIGHT = set_map_params("maps/my_second_map.map")
print(WINDOW_HEIGHT)
print(WINDOW_WIDTH)

clock = pygame.time.Clock()
pygame.display.set_caption("IT'S ME, MARIO!")
window_flags = pygame.DOUBLEBUF
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), window_flags, 32)
window.set_alpha(None)

count_iter = 0
count_to_autosave = 0
count_episodes = 0

keep_playing = start_game(count_iter, count_to_autosave, window, clock)
build_map("my_second_map")
count_map_life = 100

while keep_playing:
    if count_map_life > 0:
        count_map_life -= 1
    else:
        build_map("my_second_map")
        TILES_COUNT_X, TILES_COUNT_Y, WINDOW_HEIGHT = set_map_params("maps/my_second_map.map")
        count_map_life = 100
    count_episodes += 1
    print("Episode: ", count_episodes)
    keep_playing = start_game(count_iter, count_to_autosave, window, clock)

if not HUMAN_PLAYER:
    nn.model.save("model.h5")
    print("Model saved")
    print("Trained ", count_episodes, "episodes!")

pygame.quit()
