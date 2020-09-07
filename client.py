import time
from pickle import dumps, loads

import pygame

from game import Game
from network import Network
from player import Player

pygame.init()
pygame.font.init()

BIG_FONT = pygame.font.SysFont("comicsans", 50)
SMALL_FONT = pygame.font.SysFont("comicsans", 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

WIDTH, TOTAL_HEIGHT = 600, 665
HEIGHT = 600  # This is going to be the game board height, same as width. 
              # The additionial height is for players' information.
DIFF = TOTAL_HEIGHT - HEIGHT
window = pygame.display.set_mode((WIDTH, TOTAL_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")


def redraw(win, game, p):
    win.fill(WHITE)
    if not game.connected():
        waiting_label = BIG_FONT.render(
            "Waiting for opponent...", 1, BLACK, True)
        win.blit(waiting_label, (win.get_width() // 2 - waiting_label.get_width() //
                                 2, win.get_height() // 2 - waiting_label.get_height() // 2))
    else:
        game.board.draw(win)
        shape_label = SMALL_FONT.render(
            f"Your Shape: {p.get_shape()}", 1, BLACK)
        win.blit(shape_label, (5, HEIGHT + DIFF // 2 - 10))

        wins_label = SMALL_FONT.render(f"Total Wins: {game.get_wins(p.get_id())}", 1, BLACK)
        win.blit(wins_label, (win.get_width() -
                              wins_label.get_width() - 5, HEIGHT + DIFF // 2 - 10))

        winner = game.get_winner()
        if winner != None:  # The game ended
            pygame.draw.line(
                win, BLACK, game.get_winner_line_start(), game.get_winner_line_end(), 4)
            if winner.get_id() == p.get_id():  # We won
                winner_label = BIG_FONT.render("You Won :)", 1, GREEN)
                win.blit(winner_label, (win.get_width() // 2 -
                                        winner_label.get_width() // 2, HEIGHT // 2))

                setting_label = winner_label = BIG_FONT.render(
                    "Setting up a new game.", 1, GREEN)
                win.blit(setting_label, (win.get_width() // 2 -
                                         setting_label.get_width() // 2, HEIGHT // 2 + winner_label.get_height() + 5))
            else:  # we lost
                loser_label = BIG_FONT.render("You Lost :(", 1, RED)
                win.blit(loser_label, (win.get_width() // 2 -
                                       loser_label.get_width() // 2, HEIGHT // 2))
                setting_label = BIG_FONT.render(
                    "Setting up a new game.", 1, RED)
                win.blit(setting_label, (win.get_width() // 2 -
                                         setting_label.get_width() // 2, HEIGHT // 2 + loser_label.get_height() + 5))
        elif game.is_draw():
            draw_label = BIG_FONT.render("Draw!", 1, BLUE)
            win.blit(draw_label, (win.get_width() // 2 -
                                  draw_label.get_width() // 2, HEIGHT // 2))
            setting_label = BIG_FONT.render(
                "Setting up a new game.", 1, BLUE)
            win.blit(setting_label, (win.get_width() // 2 -
                                     setting_label.get_width() // 2, HEIGHT // 2 + draw_label.get_height() + 5))
        else:  # game is stil going
            your_turn_label = SMALL_FONT.render("Your Turn", 1, BLACK)
            his_turn_label = SMALL_FONT.render("His Turn", 1, BLACK)
            if game.get_current_turn() == p.get_id():
                win.blit(your_turn_label, (win.get_width() // 2 -
                                           your_turn_label.get_width() // 2, HEIGHT + DIFF // 2 - 10))
            else:
                win.blit(his_turn_label, (win.get_width() // 2 -
                                          his_turn_label.get_width() // 2, HEIGHT + DIFF // 2 - 10))
    pygame.display.update()


def main():
    run = True
    FPS = 60
    BOARD_SIZE = 3
    clock = pygame.time.Clock()

    try:
        con = Network("192.168.1.33", 6654)
        player = con.connect()
    except:
        print("[CLIENT] Failed creating connection. Quiting...")
        quit()

    while run:
        clock.tick(FPS)
        try:
            game = con.send("get")
        except:
            run = False
            break

        if (game == "Q"):  # The other player exited the game
            window.fill(WHITE)
            quit_label = BIG_FONT.render(
                "The other player has quit!", 1, BLACK)
            window.blit(quit_label, (window.get_width() // 2 -
                                     quit_label.get_width() // 2, window.get_height() // 2))
            directing_label = BIG_FONT.render(
                "Directing you to the main menu.", 1, BLACK)
            window.blit(directing_label, (window.get_width() // 2 -
                                          directing_label.get_width() // 2,
                                          window.get_height() // 2 + quit_label.get_height() + 5))
            pygame.display.update()
            pygame.time.delay(3000)
            con.close()
            run = False
            break

        redraw(window, game, player)
        if game.done:
            try:
                pygame.time.delay(3000)
                con.send("reset")
            except:
                break
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                if event.type == pygame.MOUSEBUTTONUP and game.connected() and \
                        game.get_current_turn() == player.get_id() and game.get_winner() == None:
                    x, y = pygame.mouse.get_pos()
                    if y < HEIGHT:
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
        start_label = BIG_FONT.render("Press anywhere to begin...", 1, BLACK)
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
