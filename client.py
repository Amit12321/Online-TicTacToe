import pygame
from pickle import dumps, loads
from game import Game
from player import Player
from network import Network

pygame.init()
pygame.font.init()

FONT = pygame.font.SysFont("comicsans", 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")


def redraw(win, game, p):
    win.fill(WHITE)
    if not game.connected():
        waiting_label = FONT.render("Waiting for opponent...", 1, BLACK, True)
        win.blit(waiting_label, (win.get_width() / 2 - waiting_label.get_width() /
                                 2, win.get_height() / 2 - waiting_label.get_height() / 2))
    else:
        game.board.draw(win)
        winner = game.get_winner()
        if winner != None:  # The game ended
            pygame.draw.line(
                win, BLACK, game.get_winner_line_start(), game.get_winner_line_end(), 4)
            if winner == p:  # We won
                winner_label = FONT.render("You Won :)", 1, (255, 0, 0))
                win.blit(winner_label, (win.get_width() // 2 -
                                        winner_label.get_width() // 2, win.get_height() // 2 - 15))
            else:  # we lost
                loser_label = FONT.render("You Lost :(", 1, (255, 0, 0))
                win.blit(loser_label, (win.get_width() // 2 -
                                       loser_label.get_width() // 2, win.get_height() // 2 - 15))
        elif game.is_draw():
            draw_label = FONT.render("Draw!", 1, (255, 0, 0))
            win.blit(draw_label, (win.get_width() // 2 -
                                  draw_label.get_width() // 2, win.get_height() // 2 - 15))
    pygame.display.update()


def main():
    run = True
    FPS = 60
    BOARD_SIZE = 3
    clock = pygame.time.Clock()
    print("WELCOME!")
    try:
        con = Network("192.168.1.36", 8820)
        player = con.get_player()
        print("Your shape is ", player.get_shape())
    except:
        print("Failed :(")
        quit()

    while run:
        clock.tick(FPS)
        try:
            game = con.send("get")
        except:
            run = False
            print("Something went bad :(")
            break
        redraw(window, game, player)
        if game.done:
            pygame.time.delay(3000)
            con.send("reset")
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                if event.type == pygame.MOUSEBUTTONUP and game.connected() and \
                        game.get_current_turn() == player.get_id() and game.get_winner() == None:
                    x, y = pygame.mouse.get_pos()
                    j = (x // (WIDTH // BOARD_SIZE))
                    i = (y // (WIDTH // BOARD_SIZE))
                    if game.board.is_available(i, j):
                        con.send(str(i) + "," + str(j))


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        window.fill(WHITE)
        start_label = FONT.render("Press mouse to begin...", 1, BLACK)
        window.blit(start_label, (window.get_width() // 2 -
                                  start_label.get_width() // 2, window.get_height() // 2 - 15))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                run = False
    main()


while True:
    menu_screen()
