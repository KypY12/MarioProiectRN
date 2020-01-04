from globals import *
from collision import *


class Player:
    def __init__(self, window, x, y, width, height):
        self.window = window
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 200, 250)
        self.collisions_dict = {"up": False, "down": False, "right": False, "left": False}

        self.vertical_momentum = 1

        self.score = 0

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect, 0)

    def move(self, nn_pressed, pressed, objects):
        collide_bonus = False
        collide_enemy = False

        move_params = [0, 0]

        if HUMAN_PLAYER:
            if pressed[pygame.K_LEFT]:
                move_params[0] -= PLAYER_MOVEMENT_SPEED
            if pressed[pygame.K_RIGHT]:
                move_params[0] += PLAYER_MOVEMENT_SPEED
            if pressed[pygame.K_UP] and self.collisions_dict["down"]:
                self.vertical_momentum = -GRAVITY
        else:
            if nn_pressed == pygame.K_LEFT:
                move_params[0] -= PLAYER_MOVEMENT_SPEED
            if nn_pressed == pygame.K_RIGHT:
                move_params[0] += PLAYER_MOVEMENT_SPEED
            if nn_pressed == pygame.K_UP and self.collisions_dict["down"]:
                self.vertical_momentum = -GRAVITY

        if not self.collisions_dict["down"]:
            if self.vertical_momentum < GRAVITY:
                self.vertical_momentum += PLAYER_MOMENTUM_STEP
            else:
                self.vertical_momentum = GRAVITY

        elif self.vertical_momentum > 0:
            self.vertical_momentum = 0

        if self.vertical_momentum < 0 and self.collisions_dict["up"]:
            self.vertical_momentum = 0

        move_params[1] += int(self.vertical_momentum)

        self.collisions_dict, check_move_params, actual_move, collide_enemy, collide_bonus, killed_enemies, is_finish = \
            move_and_collide(self.rect, move_params, objects, True)

        for b in collide_bonus:
            self.score += 1

        for killed_enemy in killed_enemies:
            self.score += 2

        self.rect.x -= actual_move[0]
        if IS_WINDOW_FOLLOW_Y:
            self.rect.y -= actual_move[1]

        if is_finish:
            return [actual_move[0], actual_move[1]], [], [], [], True

        if len(collide_enemy) > len(killed_enemies):
            return [actual_move[0], actual_move[1]], "game_over", [], [], False

        return [actual_move[0], actual_move[1]], collide_enemy, collide_bonus, killed_enemies, is_finish
