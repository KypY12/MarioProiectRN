from globals import *


class Tile:
    def __init__(self, window, x, y, width, height):
        self.window = window
        self.rect = pygame.Rect(x, y, width, height)
        if x % 40 == 0:
            self.color = (255,255,255)
        else:
            self.color = (255,50,10)

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect, 0)

    def move(self, scroll_move):
        self.rect.x -= scroll_move[0]
        if IS_WINDOW_FOLLOW_Y:
            self.rect.y -= scroll_move[1]

