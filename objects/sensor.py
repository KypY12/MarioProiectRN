from globals import *
from collision import *
from objects.bonus import Bonus
from objects.enemy import Enemy
from objects.finish import Finish
from objects.tile import Tile


class Sensor:

    def __init__(self, window, x, y, width, height):
        self.window = window
        self.rect = pygame.Rect(x, y, width, height)
        self.colors = {"air": (255, 0, 0),
                       "tile": (255, 0, 255),
                       "enemy": (0, 255, 255),
                       "bonus": (255, 255, 0),
                       "finish": (255, 100, 100)}
        self.nn_input_values = {"air": 0,
                                "tile": 1,
                                "enemy": 2,
                                "bonus": 3,
                                "finish": 4}
        self.hit = "air"

    def get_nn_input_value(self):
        return self.nn_input_values[self.hit]

    def draw(self):
        pygame.draw.rect(self.window, self.colors[self.hit], self.rect, 0)

    def move(self, scroll_movement, objects):
        # move_params = [-scroll_movement[0], -scroll_movement[1]]

        # self.rect.y += scroll_movement[1]

        collisions = get_collisions_all(self.rect, objects)

        if len(collisions) == 0:
            self.hit = "air"
        else:
            types = []
            for col in collisions:
                if type(col) == Tile:
                    types += ["tile"]
                elif type(col) == Enemy:
                    types += ["enemy"]
                elif type(col) == Bonus:
                    types += ["bonus"]
                elif type(col) == Finish:
                    types += ["finish"]

            if "enemy" in types:
                self.hit = "enemy"
            elif "finish" in types:
                self.hit = "finish"
            elif "bonus" in types:
                self.hit = "bonus"
                print("ddaaa")
            elif "tile" in types:
                self.hit = "tile"
            else:
                self.hit = "air"
