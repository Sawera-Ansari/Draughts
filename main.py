
from game import Game
from variables import *
from minimax import minimax

WINDOW = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Draughts")


def main():

    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    while run:
        clock.tick(60)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, WHITE)
            game.AI_move(new_board)

        if game.winner() != None:
            game.win(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col, row = pos[0]//80, pos[1]//80
                game.select(row, col)

        game.update()

    pygame.quit()


main()