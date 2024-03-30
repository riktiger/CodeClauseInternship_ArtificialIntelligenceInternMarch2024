# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# CodeClause Internship, March, 2024

# DOMAIN : Artificial Intelligence Intern

# PROBLEM STATEMENT : Tic-Tac-Toe AI (#CC3599)

#Create a program that allows a user to play against an AI opponent in the game of Tic-Tac-Toe. 
#Implement basic logic for the AI to make strategic moves.

# SOLUTION

# AUTHOR : ARITRA BAG

#Libraries
import sys
import pygame
import numpy as np
import random
import copy


#Constants
width = 800
height = 800
background_color = (255,255,255)
rows = 3
columns = 3
square_size = width // rows
line_color = (0,0,0)
line_width = 18
circle_color = (255,0,0)
circle_width = 15
circle_radius = square_size//4
cross_color = (0,0,255)
cross_width = 18
offset = 60



#Initializing Pygame Model
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(background_color)




class Board:
    
    def __init__(self,  squares = None):
        
        self.squares = np.zeros((rows,columns))
        self.empty = self.squares
        self.marked = 0     

    def draw_marks(self, row, column, player):
        self.squares[row][column] = player
        self.marked +=1
        
    def available_square(self, row, column):
        return self.squares[row][column] == 0
    
    def completed(self):
        return self.marked == 9
    
    def initial_state(self):
        return self.marked == 0
    
    def squares_left(self):
        squares_left = []
        for row in range(rows):
            for column in range (columns):
                if self.available_square(row, column):
                    squares_left.append((row,column))

        return squares_left

    def final_state(self, winning_line = False):
        
        #Check columns
        for column in range((columns)):
            if self.squares[0][column] == self.squares[1][column] == self.squares[2][column] != 0:
                if winning_line:
                    winning_line_color = circle_color if self.squares[0][column] == 2 else cross_color
                    win_line_start = (column*square_size + square_size // 2, offset)
                    win_line_stop = (column*square_size + square_size // 2, height - offset)
                    pygame.draw.line(screen, winning_line_color, win_line_start, win_line_stop, line_width)
                return self.squares[0][column]
            
        #Chexck rows
        for row in range((rows)):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if winning_line:
                    winning_line_color = circle_color if self.squares[row][0] == 2 else cross_color
                    win_line_start = (offset, row*square_size + square_size // 2)
                    win_line_stop = (width - offset, row*square_size + square_size // 2)
                    pygame.draw.line(screen, winning_line_color, win_line_start, win_line_stop, line_width)
                return self.squares[row][0]
            
        #Chexck top-left : bottom-right diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if winning_line:
                 winning_line_color = circle_color if self.squares[1][1] == 2 else cross_color
                 win_line_start = (offset, offset)
                 win_line_stop = (width - offset, height - offset)
                 pygame.draw.line(screen, winning_line_color, win_line_start, win_line_stop, line_width)
            
            return self.squares[row][0]
                
        #Chexck top-right : bottom-left diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if winning_line:
                 winning_line_color = circle_color if self.squares[1][1] == 2 else cross_color
                 win_line_start = (offset, height - offset)
                 win_line_stop = (width - offset, offset)
                 pygame.draw.line(screen, winning_line_color, win_line_start, win_line_stop, line_width)
            return self.squares[row][0]
                
        #No win yet
        return 0


class AI():
    
    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player
        
    def random_gameplay(self, board):
        empty_squares = board.squares_left()
        index = random.randrange(0, len(empty_squares))
        return empty_squares[index]
    
    
    def minimax (self, game_board, maximizing):
        #Terminal Case
        case = game_board.final_state()
        
        #Human Player wins
        if case == 1:
            return 1, None  #Returns board evaluation state and move
        
        
        #AI Player wins
        if case == 2:
            return -1, None  #Returns board evaluation state and move
        
        #Draw
        elif game_board.completed():
            return 0, None  #Returns board evaluation state and move
        
        #Check maximizing
        if maximizing:
            max_eval = -100000
            best_move = None
            empty_choices = game_board.squares_left()
            
            for (row,column) in empty_choices:
                temporary_board = copy.deepcopy(game_board)
                temporary_board.draw_marks (row, column, 1)
                eval = self.minimax(temporary_board, False)[0]
                                
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, column)
                    
            return max_eval, best_move
               
        #Check minimizing
        elif not maximizing:
            min_eval = 100000
            best_move = None
            empty_choices = game_board.squares_left()
            
            for (row,column) in empty_choices:
                 temporary_board = copy.deepcopy(game_board)
                 temporary_board.draw_marks (row, column, self.player)
                 eval = self.minimax(temporary_board, True)[0]
                                
                 if eval < min_eval:
                    min_eval = eval
                    best_move = (row, column)
                    
            return min_eval, best_move
            
    def eval(self, game_board):
        if self.level == 0:
            #AI plays randomly
            eval = 'random'
            move = self.random_gameplay(game_board)           
        else:
            #AI plays with MiniMax Algorithm
            eval, move = self.minimax(game_board, False)
            
        print('AI has marked the square at position ' + str(move))
            
            
        return move
        
        


class Game:
    
    def __init__(self):
        self.game_type = 'ai'
        self.ai_player = AI()
        self.player = 1 #PLayer 1 = X, Player 2 = O
        self.board = Board()
        self.run = True
        self.lines()
        #self.game_state()
        
    def game_state(self):
        if self.game_type == 'pvp':
            print('Selected game mode : Player - vs - Player ')
        elif self.game_type == 'ai' and self.ai_player.level == 0 and self.player == 1:
            print('Selected game mode : Player - vs - Computer   AI Level : Easy  Player Starts First')
        elif self.game_type == 'ai' and self.ai_player.level == 0 and self.player == 2:
            print('Selected game mode : Player - vs - Computer   AI Level : Easy  Computer Starts First')
        elif self.game_type == 'ai' and self.ai_player.level == 1 and self.player == 1:
            print('Selected game mode : Player - vs - Computer   AI Level : Hard  Player Starts First')
        elif self.game_type == 'ai' and self.ai_player.level == 1 and self.player == 2:
            print('Selected game mode : Player - vs - Computer   AI Level : Hard  Computer Starts First')
        
    def lines(self):
        screen.fill(background_color)
        #Vertical lines
        pygame.draw.line(screen, line_color, (square_size, 0), (square_size, height), line_width)
        pygame.draw.line(screen, line_color, (width - square_size, 0), (width - square_size, height), line_width)
        
        #Horizontal lines
        pygame.draw.line(screen, line_color, (0,square_size), (width,square_size), line_width)
        pygame.draw.line(screen, line_color, (0,height - square_size), (width,height - square_size), line_width)
        
    def mark(self,row,column):
        if self.player == 1:
            start_descending = (column * square_size + offset, row * square_size + offset)
            end_descending = (column * square_size + square_size - offset,  row * square_size + square_size - offset)
            pygame.draw.line(screen, cross_color, start_descending, end_descending, cross_width)
            
            start_ascending = (column * square_size + offset, row * square_size + square_size - offset)
            end_ascending = (column * square_size + square_size - offset,  row * square_size + offset)
            pygame.draw.line(screen, cross_color, start_ascending, end_ascending, cross_width)
            
        elif self.player == 2:
            center = (column * square_size + square_size // 2, row * square_size + square_size // 2)
            pygame.draw.circle(screen, circle_color, center, circle_radius, circle_width)
        
        
    def my_turn(self):
       self.player = self.player %2 +1
       
    def over(self):
        return self.board.final_state(winning_line= True) !=0 or self.board.completed()
       
    def switch_order(self):
        
        if self.player == 1:
            self.__init__()
            self.player = 2
                    
    def reset(self):
        self.__init__()
        
        


def main():
    
    #Objects
    game = Game()
    board = game.board
    ai_player = game.ai_player
    game.game_state()
    
    while True:
          
        
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.game_type = 'pvp'
                    game.game_state()
                  
                if event.key == pygame.K_i:
                    game.game_type = 'ai'
                    game.game_state()
                                    
                if event.key == pygame.K_0:
                    ai_player.level = 0
                    game.game_state()
                        
                if event.key == pygame.K_1:
                    ai_player.level = 1
                    game.game_state()
                    
                if event.key == pygame.K_r:
                    print ('Game has been reset')
                    game.reset()
                    board = game.board
                    ai_player = game.ai_player
                    game.game_state()
                    
                if event.key == pygame.K_s:
                        print ('Computer will start first now, press reset to make player start first')
                        game.switch_order()
                        game.game_state()
                        board = game.board
                        ai_player = game.ai_player
                              
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1]//square_size
                column = pos[0]//square_size
                
                if board.available_square(row,column) and game.run:
                    board.draw_marks(row,column,game.player)
                    game.mark(row,column)
                    game.my_turn()
                    
                    if game.over():
                        game.run = False
                    
                                                
            if game.game_type =='ai' and game.player == ai_player.player and game.run:
                pygame.display.update()
                row, column = ai_player.eval(board)
                board.draw_marks(row,column,game.player)
                game.mark(row,column)
                game.my_turn()
                
                if game.over():
                    game.run = False
                
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
                
        pygame.display.update()
                
                
main()
