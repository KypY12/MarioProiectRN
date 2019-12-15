from globals import *


class Bonus:
    def __init__(self, window, x, y, width, height):
        self.window = window
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (250,150,200)

    def draw(self, scroll_move):
        self.rect.x -= scroll_move[0]
        pygame.draw.rect(self.window, self.color, self.rect, 0)