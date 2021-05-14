
from variables import *


class Piece:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 80 * self.col + 40
        self.y = 80 * self.row + 40


    def draw_piece(self, window):
        pygame.draw.circle(window, (127, 127, 127), (self.x, self.y), 30)
        pygame.draw.circle(window, self.color, (self.x, self.y), 28)
        if self.king == True:
            window.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))


    def move_piece(self, row, col):
        self.row = row
        self.col = col
        self.x = 80 * self.col + 40
        self.y = 80 * self.row + 40