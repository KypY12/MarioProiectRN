import sys
import time

import pygame.locals

from helpers.mapfunctions import *
from helpers.otherfunctions import *


def start_game():

    def gg_wp(window, score):
        font_1 = pygame.font.Font('freesansbold.ttf', 64)
        font_2 = pygame.font.Font('freesansbold.ttf', 32)

        game_over_text = font_1.render('GG WP', True, (0, 255, 0))
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
        window.blit(game_over_text, game_over_text_rect)

        score_text = font_2.render("Score : "+str(score), True, (0, 255, 0))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)
        window.blit(score_text, score_text_rect)

        pygame.display.flip()


    def game_over(window, score):
        font_1 = pygame.font.Font('freesansbold.ttf', 64)
        font_2 = pygame.font.Font('freesansbold.ttf', 32)

        game_over_text = font_1.render('Game over', True, (255, 0, 0))
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
        window.blit(game_over_text, game_over_text_rect)

        score_text = font_2.render("Score : "+str(score), True, (255, 0, 0))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)
        window.blit(score_text, score_text_rect)

        pygame.display.flip()

    pygame.init()

    TILES_COUNT_X, TILES_COUNT_Y, WINDOW_HEIGHT, tiles, player, enemies, bonuses, finish_states = load_map("maps/my_first_map.map")

    clock = pygame.time.Clock()
    pygame.display.set_caption("IT'S ME, running from the unleashed wolves!")
    print(WINDOW_HEIGHT)
    print(WINDOW_WIDTH)
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

    for tile in tiles:
        tile.window = window

    for enemy in enemies:
        enemy.window = window

    for bonus in bonuses:
        bonus.window = window

    for finish in finish_states:
        finish.window = window

    player.window = window

    while True:
        window.fill((0, 0, 0))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        enemy_hit = False
        for enemy in enemies:
            if enemy.move([player] + tiles):
                enemy_hit = True
                break
        if enemy_hit:
            game_over(window, player.score)
            break

        scroll_params, collide_enemy, collide_bonus, killed_enemies, is_win = player.move(pressed, tiles + enemies + bonuses + finish_states)

        if is_win:
            gg_wp(window, player.score)
            break

        for killed in killed_enemies:
            if killed in enemies:
                enemies.remove(killed)

        if player.rect.y > WINDOW_HEIGHT:
            game_over(window, player.score)
            break

        for bonus in collide_bonus:
            if bonus in bonuses:
                bonuses.remove(bonus)

        if collide_enemy == "game_over":
            game_over(window, player.score)
            break

        draw_objects(tiles + enemies + bonuses + finish_states + [player], scroll_params)
        pygame.display.flip()
        clock.tick(TICK_RATE)

    time.sleep(2)
    return True
    # pressed = pygame.key.get_pressed()
    # while not pressed[pygame.K_KP_ENTER] or not pressed[pygame.K_KP_ENTER]:
    #     pressed = pygame.key.get_pressed()
    #     time.sleep(1)
    #
    # if pressed[pygame.K_SPACE]:
    #     return True
    # elif pressed[pygame.K_ESCAPE]:
    #     return False


keep_playing = start_game()
while keep_playing:
    start_game()

pygame.quit()

#
#
#
# class Player:
#     def __init__(self, x, y, width, height, move_step):
#         self.rect = pygame.Rect(x+PLAYER_BACK_OFFSET, y+PLAYER_UP_OFFSET, width, height)
#         self.color = (255, 100, 150)
#         self.move_step = move_step
#         self.colisions_dict = {"up": False, "down": False, "right": False, "left": False}
#         self.vertical_momentum = 0
#         self.max_vertical_momentum = gravity
#         self.increasing_momentum = 1
#         self.jump_vertical_momentum = -21
#
#     def draw(self, scroll_move):
#         self.rect.x -= scroll_move[0]
#         # self.rect.y -= scroll_move[1]
#         pygame.draw.rect(window, self.color, self.rect, 0)
#
#     def move(self, pressed, objects):
#         other_objects = [obj.rect for obj in objects if obj.rect != self.rect]
#         move_params = [0, 0]
#         if pressed[pygame.K_LEFT]:
#             move_params[0] -= self.move_step
#         if pressed[pygame.K_RIGHT]:
#             move_params[0] += self.move_step
#         if pressed[pygame.K_SPACE] and self.colisions_dict["down"]:
#             self.vertical_momentum = self.jump_vertical_momentum
#
#         if not self.colisions_dict["down"]:
#             move_params[1] += self.vertical_momentum
#         self.vertical_momentum += self.increasing_momentum
#         if self.vertical_momentum > self.max_vertical_momentum or self.colisions_dict["up"]:
#             self.vertical_momentum = self.max_vertical_momentum
#
#         # if self.colisions_dict["left"] and move_params[0] < 0:
#         #     move_params[0] = 0
#         # if self.colisions_dict["right"] and move_params[0] > 0:
#         #     move_params[0] = 0
#         # if self.colisions_dict["up"] and move_params[1] < 0:
#         #     move_params[1] = 0
#         # if self.colisions_dict["down"] and move_params[1] > 0:
#         #     move_params[1] = 0
#
#         self.colisions_dict, check_move_params = move_and_collide(self.rect, move_params, other_objects)
#
#         # move_params[1]*check_move_params[1]
#         return [[move_params[0]*check_move_params[0], move_params[1]*check_move_params[1]], [self.rect.x, self.rect.y]]
#
#
# class Enemy:
#     def __init__(self, x, y, width, height):
#         self.rect = pygame.Rect(x, y, width, height)
#         self.color = (100, 200, 50)
#         self.move_step = 5
#         self.move_max_count = 30
#         self.move_count = self.move_max_count
#         self.colisions_dict = {"up": False, "down": False, "right": False, "left": False}
#         self.direction = "right"
#
#     def draw(self, scroll_move):
#         self.rect.x -= scroll_move[0]
#         # self.rect.y -= scroll_move[1]
#         pygame.draw.rect(window, self.color, self.rect, 0)
#
#     def move_on_direction(self):
#         if self.direction == "up":
#             self.rect.y -= self.move_step
#         elif self.direction == "down":
#             self.rect.y += self.move_step
#         elif self.direction == "left":
#             self.rect.x -= self.move_step
#         elif self.direction == "right":
#             self.rect.x += self.move_step
#
#     def set_op_dir(self):
#         if self.direction == "left":
#             self.direction = "right"
#         elif self.direction == "right":
#             self.direction = "left"
#         elif self.direction == "up":
#             self.direction = "down"
#         else:
#             self.direction = "up"
#
#     def move(self, objects):
#         other_objects = [obj.rect for obj in objects if obj.rect != self.rect]
#         move_params = [0, 0]
#
#         if self.move_count > 0:
#             self.move_on_direction()
#             self.move_count -= 1
#         else:
#             self.set_op_dir()
#             self.move_count = self.move_max_count
#
#         self.colisions_dict, check_move_params = move_and_collide(self.rect, move_params, other_objects)
#
#         if self.colisions_dict["up"] and self.direction == "up":
#             if self.colisions_dict["right"]:
#                 self.direction = "left"
#             else:
#                 self.direction = "right"
#         elif self.colisions_dict["down"] and self.direction == "down":
#             if self.colisions_dict["right"]:
#                 self.direction = "left"
#             else:
#                 self.direction = "right"
#         elif self.colisions_dict["left"] and self.direction == "left":
#             if self.colisions_dict["up"]:
#                 self.direction = "down"
#             else:
#                 self.direction = "up"
#         elif self.colisions_dict["right"] and self.direction == "right":
#             if self.colisions_dict["up"]:
#                 self.direction = "down"
#             else:
#                 self.direction = "up"
#
#         # move_params[1]*check_move_params[1]
#         # return [[move_params[0]*check_move_params[0], move_params[1]*check_move_params[1]], [self.rect.x, self.rect.y]]
#
#
# class Object:
#     def __init__(self, x, y, width, height):
#         self.rect = pygame.Rect(x, y, width, height)
#         self.color = (255, 255, 255)
#
#     def draw(self, scroll_move):
#         self.rect.x -= scroll_move[0]
#         # self.rect.y -= scroll_move[1]
#         pygame.draw.rect(window, self.color, self.rect, 0)
