import pygame
from player import Player

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 600, 600

class PositionTaken(Exception):
    def __init__(self, arg):
        self.arg = arg

class Board:
    def __init__(self, size):
        self.size = size
        self.bo = [["" for i in range(size)] for j in range(size)]
        self.is_full = False
        self.empty_places = size ** 2
        self.winner = None
        self.winner_start = None # this will help us later drawing the winning line
        self.winner_end = None # ""

    def draw(self, window): #draw the board on window
        w = window.get_width()
        len = w // self.size
        for i in range(self.size + 1): #draw rows
            pygame.draw.line(window, BLACK, (0, i * len), (w, i * len), 3)
        for i in range(self.size + 1): #draw cols
            pygame.draw.line(window, BLACK, (i * len, 0), (i * len, w), 3)
        
        for i in range(self.size):
            for j in range(self.size):
                if self.bo[i][j] == "O":
                    pygame.draw.circle(window, BLACK, (j * len + len//2, i * len + len//2), len // 3, 3)
                if self.bo[i][j] == "X":
                    pygame.draw.line(window, BLACK, (len // 5 + j * len, i * len + len // 5), (j * len + len - len // 5, i* len + len - len // 5), 3)
                    pygame.draw.line(window, BLACK, (j * len + len - len // 5, i * len + len // 5), (j * len + len // 5, i * len + len - len // 5), 3)

    def init_board(self):
        self.bo = [["" for i in range(self.size)] for j in range(self.size)]
        self.is_full = False
        self.empty_places = self.size ** 2

    def is_available(self, i, j,):
        return self.bo[i][j] == ""
    
    def assign(self, shape, i, j):
        if (not self.is_available(i, j)):
            raise PositionTaken("This position is taken. Choose a different one")
        else:
            self.bo[i][j] = shape
            self.empty_places -= 1
            if (self.empty_places == 0):
                self.is_full = True
    
    def check_for_winner(self, player, i, j): #Player [shape] chose bo[i][j] pos. check if he wins
        len = WIDTH // self.size
        winner_seq = [player.shape for h in range(self.size)]
        if self.bo[i] == winner_seq: #check row
            self.winner_start = (0, i * len + len // 2)
            self.winner_end = (WIDTH, i * len + len // 2)
            self.winner = player
            return True
        elif [self.bo[h][j] for h in range(self.size)] == winner_seq: #check col
            self.winner_start = (j * len + len // 2, 0)
            self.winner_end = (j * len + len // 2, WIDTH)
            self.winner = player
            return True
        else:
            if i == j:
                if [self.bo[h][h] for h in range(self.size)] == winner_seq: #check main diagonal
                    self.winner_start = (0, 0)
                    self.winner_end = (WIDTH, WIDTH)
                    self.winner = player
                    return True
            elif  i + j == self.size - 1:
                if [self.bo[self.size - 1 - h][h] for h in range(self.size)] == winner_seq: #check secondary diagonal
                    self.winner_start = (WIDTH, 0)
                    self.winner_end = (0, WIDTH)
                    self.winner = player
                    return True
        return False

    def check_if_full(self):
        return self.is_full

class Game:
    def __init__(self, game_id, board_size):
        self.game_id = game_id
        self.board_size = board_size
        self.ready = False
        self.board = Board(board_size)
        self.current_turn = 0
        self.done = False
    
    def make_move(self, player, i, j):
        try:
            self.board.assign(player.shape, i, j)
        except PositionTaken as p:
            print(p)
    
    def connected(self):
        return self.ready

    def is_draw(self):
        return self.board.is_full
    
    def get_winner(self):
        return self.board.winner

    def get_winner_line_start(self):
        return self.board.winner_start
    
    def get_winner_line_end(self):
        return self.board.winner_end
    
    def get_current_turn(self):
        return self.current_turn
    
    def reset(self):
        self.board.init_board()
        self.current_turn = 0
        self.done = False
