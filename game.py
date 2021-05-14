
from variables import *
from board import Board


class Game:

    def __init__(self, window):
        self.selected_piece = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.window = window


    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves()
        pygame.display.update()


    def winner(self):
        result = self.board.winner()
        return result


    def win(self, result):
        if result == BLACK:
            self.window.blit(WON, (100, 200))
        elif result == WHITE:
            self.window.blit(LOST, (100, 200))
        pygame.display.update()
        pygame.time.wait((3000))


    def draw_valid_moves(self):
        for move in self.valid_moves:
            row, col = move
            pygame.draw.circle(self.window, (0, 255, 0), (col * 80 + 40, row * 80 + 40), 15)


    def select(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected_piece:
            if piece == '' and (row, col) in self.valid_moves:
                self.board.move(self.selected_piece, row, col)
                skipped = self.valid_moves[(row, col)]
                if skipped:
                    self.board.remove(skipped)
                self.change_turn()
            else:
                self.selected_piece = None
                self.select(row, col)
        else:
            if piece != '' and self.turn == BLACK:
                self.selected_piece = piece
                self.valid_moves = self.board.get_valid_moves(self.selected_piece)
                return True
        return False


    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK


    def get_board(self):
        return self.board


    def AI_move(self, board):
        self.board = board
        self.change_turn()