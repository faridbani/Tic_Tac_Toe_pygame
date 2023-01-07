# Tic TacToe with AI

import copy
import random
import pygame
import sys
import numpy as np

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, S_HIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)
menu_surface = pygame.Surface(MENU_SIZE)
menu_surface.fill(MENU_COLOR)

bfont = pygame.font.SysFont("Arial", 20, bold=True)

class Button:
    def __init__(self, text) -> None:
        self.text = bfont.render(text, 1, LINE_COLOR, MENU_COLOR)
        self.size = self.text.get_size()
        self.text_surface = pygame.Surface(self.size)
        #self.text_surface.fill(BG_COLOR)

    def show(self):
        self.text_surface.blit(self.text, (0, 0))
        menu_surface.blit(self.text_surface, (10, 10))

class Board:
    def __init__(self) -> None:
        self.squers = np.zeros((COLS, ROWS), dtype=np.int32)
        self.empty_sqrs = self.squers # [empty]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        ''' 
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # vertical win
        for col in range(COLS):
            if self.squers[0][col] ==  self.squers[1][col] ==  self.squers[2][col] != 0:
                if show:
                    sPos = (col * SQUER_SIZE + SQUER_SIZE // 2, MENU_HIGHT)
                    ePos = (col * SQUER_SIZE + SQUER_SIZE // 2, HIGHT + MENU_HIGHT)
                    pygame.draw.line(screen, WIN_COLOR, sPos, ePos, LINE_WIDTH)
                return self.squers[0][col]
        # horizontal win
        for row in range(ROWS):
            if self.squers[row][0] ==  self.squers[row][1] ==  self.squers[row][2] != 0:
                if show:
                    sPos = (0, row * SQUER_SIZE + SQUER_SIZE // 2 + MENU_HIGHT)
                    ePos = (WIDTH, row * SQUER_SIZE + SQUER_SIZE // 2 + MENU_HIGHT)
                    pygame.draw.line(screen, WIN_COLOR, sPos, ePos, LINE_WIDTH)
                return self.squers[row][0]
        # desc diagonal
        if self.squers[0][0] ==  self.squers[1][1] ==  self.squers[2][2] != 0:
            if show:
                sPos = (0, MENU_HIGHT)
                ePos = (WIDTH, HIGHT + MENU_HIGHT)
                pygame.draw.line(screen, WIN_COLOR, sPos, ePos, LINE_WIDTH)
            return self.squers[1][1]

        # asc diagonal
        if self.squers[2][0] ==  self.squers[1][1] ==  self.squers[0][2] != 0:
            if show:
                sPos = (WIDTH, MENU_HIGHT)
                ePos = (0, HIGHT + MENU_HIGHT)
                pygame.draw.line(screen, WIN_COLOR, sPos, ePos, LINE_WIDTH)
            return self.squers[1][1]

        # no win yet
        return 0


    def mark_sqr(self, row, col, player):
        self.squers[row][col] = player
        self.marked_sqrs += 1

    def empty_squer(self, row, col):
        return self.squers[row][col] == 0

    def isfull(self):
        return self.marked_sqrs == 9

    def empty_sqes(self):
        return self.marked_sqrs == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_squer(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rand(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    def minimax(self, board, maximizing):
        # Terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move
        # player 2 (ai) wins
        if case == 2:
            return -1, None
        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rand(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        #print(f'AI has chosen to mark in squre at pos {move} with eval of: {eval}')
        return move




class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.show_lines()
        self.player = 1
        self.gamemode = 'ai' # ai vs pvp
        self.running = True
        self.ai = AI()

    def show_lines(self):
        # set bg
        screen.fill(BG_COLOR)
        # vertical lines
        pygame.draw.line(screen, LINE_COLOR, (0, MENU_HIGHT), (WIDTH, MENU_HIGHT), 5)
        pygame.draw.line(screen, LINE_COLOR, (0, SQUER_SIZE+MENU_HIGHT), (WIDTH, SQUER_SIZE+MENU_HIGHT), 5)
        pygame.draw.line(screen, LINE_COLOR, (0, HIGHT - SQUER_SIZE+MENU_HIGHT), (WIDTH, HIGHT - SQUER_SIZE+MENU_HIGHT), 5)
        # horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (SQUER_SIZE, MENU_HIGHT), (SQUER_SIZE, HIGHT+MENU_HIGHT), 5)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUER_SIZE, MENU_HIGHT), (WIDTH - SQUER_SIZE, HIGHT+MENU_HIGHT), 5)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_player()
    
    def next_player(self):
        self.player = self.player %2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
    
    def reset(self):
        self.__init__()

    def gameover(self):
        return self.board.final_state(True) != 0 or self.board.isfull()
    
    def draw_fig(self, row, col):
        if self.player == 1:
            # a cross
            # desc-line
            start_desc = (col * SQUER_SIZE + OFFSET, row * SQUER_SIZE + OFFSET + MENU_HIGHT)
            end_desc = (col * SQUER_SIZE + SQUER_SIZE - OFFSET, row * SQUER_SIZE + SQUER_SIZE - OFFSET + MENU_HIGHT)
            pygame.draw.line(screen, LINE_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc-line
            start_asc = (col * SQUER_SIZE + OFFSET, row * SQUER_SIZE + SQUER_SIZE  - OFFSET + MENU_HIGHT)
            end_asc = (col * SQUER_SIZE + SQUER_SIZE - OFFSET, row * SQUER_SIZE + OFFSET + MENU_HIGHT)
            pygame.draw.line(screen, LINE_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # a circle
            center = (col * SQUER_SIZE + SQUER_SIZE // 2, row * SQUER_SIZE + SQUER_SIZE // 2 + MENU_HIGHT )
            pygame.draw.circle(screen, CIRC_COLOR, center, RADUS, CIRC_WIDTH)

# main
def main():
    game = Game()
    reset_button = Button("Reset")
    board = game.board
    ai = game.ai
    # The main loop
    while True:
        screen.blit(menu_surface, (0, 0))
        reset_button.show()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # change the gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                
                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1
                
                # reset the game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
         
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] > MENU_HIGHT:
                    #print(pos)
                    col = pos[0] // SQUER_SIZE
                    row = (pos[1] - MENU_HIGHT) // SQUER_SIZE

                    if board.empty_squer(row, col) and game.running:
                        game.make_move(row, col)

                        if game.gameover():
                            game.running = False
                else:
                    if 10 < pos[0] < reset_button.size[0] + 10:
                        game.reset()
                        board = game.board
                        ai = game.ai

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # update the screen
            pygame.display.update()

            # ai methods
            row, col = ai.eval(board)
            game.make_move(row, col)
            if game.gameover():
                game.running = False     

        pygame.display.update()

main()

