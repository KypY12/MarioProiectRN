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

    def draw(self, scroll_movement):
        self.rect.x -= scroll_movement[0]
        pygame.draw.rect(self.window, self.color, self.rect, 0)

    def move(self, pressed, objects):
        # other_objects = [obj for obj in objects if obj.rect != self.rect]
        if self in objects:
            objects.remove(self)

        collide_bonus = False
        collide_enemy = False

        move_params = [0, 0]

        if pressed[pygame.K_LEFT]:
            move_params[0] -= PLAYER_MOVEMENT_SPEED
        if pressed[pygame.K_RIGHT]:
            move_params[0] += PLAYER_MOVEMENT_SPEED
        if pressed[pygame.K_UP] and self.collisions_dict["down"]:
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

        move_params[1] += self.vertical_momentum

        self.collisions_dict, check_move_params, collide_enemy, collide_bonus, killed_enemies, is_finish = move_and_collide(self.rect, move_params, objects, True)

        for b in collide_bonus:
            self.score += 1

        if is_finish:
            return [], [], [], [], True

        if len(collide_enemy) > len(killed_enemies):
            return [], "game_over", [], [], False

        return [move_params[0]*check_move_params[0], move_params[1]*check_move_params[1]], collide_enemy, collide_bonus, killed_enemies, is_finish
