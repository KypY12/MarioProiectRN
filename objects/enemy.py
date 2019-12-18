from globals import *
import collision


class Enemy:
    def __init__(self, window, x, y, width, height):
        self.window = window
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (250, 200, 100)

        self.move_params = [0, 0]
        self.move_step = 5
        self.move_max_count = 500
        self.move_count = self.move_max_count
        self.collisions_dict = {"up": False, "down": False, "right": False, "left": False}
        self.direction = "right"

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect, 0)

    def move_on_direction(self):
        if self.direction == "up":
            self.move_params[1] -= self.move_step
        elif self.direction == "down":
            self.move_params[1] += self.move_step
        elif self.direction == "left":
            self.move_params[0] -= self.move_step
        elif self.direction == "right":
            self.move_params[0] += self.move_step

    def set_op_dir(self):
        if self.direction == "left":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "left"
        elif self.direction == "up":
            self.direction = "down"
        else:
            self.direction = "up"

    def move(self, objects, scroll_movement):
        # other_objects = [obj.rect for obj in objects if obj.rect != self.rect]
        if self in objects:
            objects.remove(self)

        self.move_params = [0, 0]

        if self.move_count > 0:
            self.move_on_direction()
            self.move_count -= self.move_step
        else:
            self.set_op_dir()
            self.move_count = self.move_max_count

        self.collisions_dict, check_move_params, not_used_1, check_if_player, not_used_2, not_used_3 = collision.move_and_collide(self.rect, self.move_params, objects, False)

        self.rect.x -= scroll_movement[0]

        if check_if_player:
            return True

        # if self.collisions_dict["up"] and self.direction == "up":
        #     if self.collisions_dict["right"]:
        #         self.direction = "left"
        #     else:
        #         self.direction = "right"
        # elif self.collisions_dict["down"] and self.direction == "down":
        #     if self.collisions_dict["right"]:
        #         self.direction = "left"
        #     else:
        #         self.direction = "right"
        # elif self.collisions_dict["left"] and self.direction == "left":
        #     if self.collisions_dict["up"]:
        #         self.direction = "down"
        #     else:
        #         self.direction = "up"
        # elif self.collisions_dict["right"] and self.direction == "right":
        #     if self.collisions_dict["up"]:
        #         self.direction = "down"
        #     else:
        #         self.direction = "up"

        return False
        # self.move_params = [0, 0]
        # move_params[1]*check_move_params[1]
        # return [[move_params[0]*check_move_params[0], move_params[1]*check_move_params[1]], [self.rect.x, self.rect.y]]
