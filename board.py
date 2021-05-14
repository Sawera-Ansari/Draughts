
from piece import Piece
from variables import *


class Board:

    def __init__(self):
        self.board = []
        self.white_pieces = self.black_pieces = 12
        self.white_kings = self.black_kings = 0
        self.set_board()


    def draw_board(self, window):
        window.fill(BLACK)
        for row in range (0, 8):
            if row % 2 == 0:
                for col in range(1, 8, 2):
                    pygame.draw.rect(window, (160, 160, 160), (row*80, col*80, 80, 80))
            else:
                for col in range(0, 8, 2):
                    pygame.draw.rect(window, (160, 160, 160), (row*80, col*80, 80, 80))


    def set_board(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append('')
                else:
                    self.board[row].append('')


    def draw(self, window):
        self.draw_board(window)
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '':
                    piece.draw_piece(window)


    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = ''
            if piece != '':
                if piece.color == BLACK:
                    self.black_pieces -= 1
                else:
                    self.white_pieces -= 1


    def winner(self):
        if self.black_pieces <= 0:
            return WHITE
        elif self.white_pieces <= 0:
            return BLACK

        return None


    def evaluate(self):
        return self.white_pieces - self.black_pieces + (0.5 * (self.white_kings - self.black_kings))


    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != '' and piece.color == color:
                    pieces.append(piece)
        return pieces


    def move(self, piece, row, col):
        self.board[row][col], self.board[piece.row][piece.col] = self.board[piece.row][piece.col], self.board[row][col]
        piece.move_piece(row, col)
        if row == 7 or row == 0:
            piece.king = True
            if piece.color == (0, 0, 0):
                self.black_kings += 1
            else:
                self.white_kings +=1


    def get_piece(self, row, col):
        return self.board[row][col]


    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self.search_left(piece, row, left, -1))
            moves.update(self.search_right(piece, row, right, -1))

        if piece.color == WHITE or piece.king:
            moves.update(self.search_left(piece, row, left, 1))
            moves.update(self.search_right(piece, row, right, 1))

        return moves


    def search_left(self, piece, row, left, direction, skipped=[]):
        moves = {}
        pieces = []
        if left >= 0 and ((direction == -1 and row <= 7 and not row <= 0) or (direction == 1 and row >= 0 and not row >= 7)):
            temp_piece = self.board[row + direction][left]
            if temp_piece == '':

                if 0 <= left + 1 <= 7 and self.board[row][left + 1] != '':
                    if not skipped:
                        moves.update({(row + direction, left): skipped})

                    elif skipped:
                        moves.update({(row + direction, left): skipped})

                        row = row + direction
                        left = left - 1
                        if left > 0 and not (row <= 0 or row >= 7):
                            temp2_piece = self.board[row + direction][left]

                            if temp2_piece != '' and temp2_piece.color != piece.color:
                                moves.update(self.search_left(piece, row, left, direction, skipped + pieces))

                            left = left + 2
                            if 0 <= left <= 7:
                                temp2_piece = self.board[row + direction][left]

                                if temp2_piece != '' and temp2_piece.color != piece.color:
                                    moves.update(self.search_right(piece, row, left, direction, skipped + pieces))

            elif temp_piece.color != piece.color:
                row = row + direction
                left = left - 1
                if left >= 0 and not (row <= 0 or row >= 7):
                    temp2_piece = self.board[row + direction][left]
                    if temp2_piece == '':
                        pieces += [temp_piece]
                        moves.update(self.search_left(piece, row, left, direction, skipped + pieces))
                        moves.update(self.search_right(piece, row, left, direction, skipped + pieces))

        return moves


    def search_right(self, piece, row, right, direction, skipped=[]):
        moves = {}
        pieces = []
        if right <= 7 and ((direction == -1 and row <= 7 and not row <= 0) or (direction == 1 and row >= 0 and not row >= 7)):
            temp_piece = self.board[row + direction][right]
            if temp_piece == '':
                if 0 <= right - 1 <= 7 and self.board[row][right - 1] != '':

                    if not skipped:
                        moves.update({(row + direction, right): skipped})

                    elif skipped:
                        moves.update({(row + direction, right): skipped})

                        row = row + direction
                        right = right + 1
                        if right < 7 and not (row <= 0 or row >= 7):

                            temp2_piece = self.board[row + direction][right]

                            if temp2_piece != '' and temp2_piece.color != piece.color:
                                moves.update(self.search_right(piece, row, right, direction, skipped + pieces))

                            right = right - 2
                            if 0 <= right <= 7:
                                temp2_piece = self.board[row + direction][right]

                                if temp2_piece != '' and temp2_piece.color != piece.color:
                                    moves.update(self.search_left(piece, row, right, direction, skipped + pieces))

            elif temp_piece.color != piece.color:
                row += direction
                right += 1
                if right <= 7 and not (row <= 0 or row >= 7):
                    temp2_piece = self.board[row + direction][right]
                    if temp2_piece == '':
                        pieces += [temp_piece]
                        moves.update(self.search_right(piece, row, right, direction, skipped + pieces))
                        moves.update(self.search_left(piece, row, right, direction, skipped + pieces))

        return moves