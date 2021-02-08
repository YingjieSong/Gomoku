'''
https://en.wikipedia.org/wiki/Gomoku#Variations
Free-style gomoku requires a row of five or more stones for a win.
Standard gomoku requires a row of exactly five stones for a win: rows of six or more, called overlines, do not count.
'''

import pygame
import re

class Game:
    grid_size = 40     # side length (in pixels) of a single grid
    p1_cur = True      # current player is p1 (holds black stones)
    game_end = False   # game ends
    hist = []          # history of moves
    window_color = pygame.Color('Wheat')
    line_color = pygame.Color('Black')
    line_width = 1
    border_line_width = 2
    border_padding = 5
    border_color = pygame.Color('Black')
    p1_color = pygame.Color('Black')
    p2_color = pygame.Color('White')

    def __init__(self, intersect_num = 15):
        pygame.init()
        self.intersect_num = intersect_num # number of intersections, default 15x15 board
        self.grid_num = intersect_num - 1 # number of grids
        self.board = ['0' * intersect_num for y in range(intersect_num)] # underlying array
        self.window_size = self.grid_size * (self.grid_num + 2)
        self.border_lenth = self.grid_size * self.grid_num + self.border_padding * 2
        self.zero_point = self.grid_size - self.border_padding

        self.font = pygame.font.SysFont("Times New Roman", 20)
        self.window = pygame.display.set_mode((self.window_size, self.window_size))

    def run(self):
        self.__draw_board()
        while True:
            for event in pygame.event.get():
                rc = self.__on_event(event)
                if rc == 1:
                    pygame.quit()
                    exit()

    def __on_event(self, event):
        if event.type == pygame.QUIT:
            return 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                (pos_x, pos_y) = event.pos
                x = (pos_x - self.grid_size // 2) // self.grid_size
                y = (pos_y - self.grid_size // 2) // self.grid_size
                if not self.game_end:
                    if self.board[y][x] != '0':
                        return
                    self.__draw(x, y)

    def __draw_board(self):
        self.window.fill(self.window_color)
        # draw border
        pygame.draw.rect(self.window, self.border_color, (self.zero_point, self.zero_point, self.border_lenth, self.border_lenth), self.border_line_width)
        # draw grids
        for i in range(self.grid_num):
            for j in range(self.grid_num):
                pygame.draw.rect(self.window, self.line_color, (self.grid_size * (i + 1), self.grid_size * (j + 1), self.grid_size + 1, self.grid_size + 1), self.line_width)
                if i == 3 and (j == 3 or j == self.grid_num - 3) or \
                        i == self.grid_num - 3 and (j == 3 or j == self.grid_num - 3) or \
                        i == self.grid_num / 2 and j == self.grid_num / 2:
                    pygame.draw.circle(self.window, self.line_color, (self.grid_size * (i + 1),self.grid_size * (j + 1)), 5)
        pygame.display.update()

    def __draw(self, x, y):
        if x in range(self.intersect_num) and y in range(self.intersect_num):
            pygame.draw.circle(self.window, self.p1_color if self.p1_cur else self.p2_color, ((x + 1) * self.grid_size, (y + 1) * self.grid_size), 18)
            pygame.display.update()
            self.hist.append((x, y))
            temp = self.board[y]
            temp = temp[:x] + ('1' if self.p1_cur else '2') + temp[x+1:]
            self.board[y] = temp
            self.__check()
            self.p1_cur = not self.p1_cur

    def __check(self):
        '''
        checking logic is learned from https://stackoverflow.com/a/4419699
        '''
        # row
        text1 = '0'.join(str(s) for s in self.board)
        obj1 = re.search('([^1]|^)1{5}([^1]|$)|([^2]|^)2{5}([^2]|$)', text1)
        
        # column
        trans_board = [''.join(s) for s in zip(*self.board)] # transpose
        text2 = '0'.join(str(s) for s in trans_board)
        obj2 = re.search('([^1]|^)1{5}([^1]|$)|([^2]|^)2{5}([^2]|$)', text2)
        
        # upper-left to lower-right diagonal
        board3 = []
        for i in range(self.intersect_num):
            board3.append('0' * i + self.board[i] + '0' * (self.intersect_num - 1 - i))
        board3 = [''.join(s) for s in zip(*board3)] # transpose
        text3 = '0'.join(str(s) for s in board3)
        obj3 = re.search('([^1]|^)1{5}([^1]|$)|([^2]|^)2{5}([^2]|$)', text3)
        
        # lower-left to upper-right diagonal
        board4 = []
        for i in range(self.intersect_num):
            board4.append('0' * (self.intersect_num - 1 - i) + self.board[i] + '0' * i)
        board4 = [''.join(s) for s in zip(*board4)] # transpose
        text4 = '0'.join(str(s) for s in board4)
        obj4 = re.search('([^1]|^)1{5}([^1]|$)|([^2]|^)2{5}([^2]|$)', text4)

        # end the game
        if obj1 or obj2 or obj3 or obj4:
            self.game_end = True
            render = self.font.render("BLACK WIN!" if self.p1_cur else "WHITE WIN!", 1, pygame.Color('red'))
            self.window.blit(render, (self.grid_size * (self.grid_num / 2) - 15, 0))
            pygame.display.update()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()