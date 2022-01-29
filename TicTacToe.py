#!/usr/bin/env python3

'''

** My personal version of one of the most popular first python project: tictactoe. **

'''

import numpy as np
import random
import time

class Game:
    
    def __init__(self):
        self.board = np.array([''] * 9).reshape(3, 3) # game board
        self.current_winner = False
    
    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
    
    # print board number 0-8    
    def print_board_num(self): 
        ls = np.arange(9).reshape(3,3)
        for row in ls:
            print(str(row))
    
    # return an array with indices of empty squares
    def available_moves(self): 
        available_moves = np.where(self.board.reshape(-1) == '')
        return available_moves
    
    # this method will return TRUE in case of no empty square
    def is_full(self):
        if all(self.board.reshape(-1) != ''):
            return True
    
    # insert Player.player attribute (x or o) into the square
    def players_move(self, square, player): 
        self.board = self.board.reshape(-1)
        self.board[square] = player
        self.board = self.board.reshape(3, 3)
    
    # update self.current_winner in case of winner
    def winner(self, player): 
        #check rows
        for row in self.board:
            if len([i for i in row if i == player]) == 3:
                self.current_winner = player 
            
        #check cols
        for col in np.transpose(self.board):
            if len([i for i in col if i == player]) == 3:
                self.current_winner = player 
        
        #check diag
        if (self.board[0,0] == player) and (self.board[1,1] == player) and (self.board[2,2] == player):
             self.current_winner = player
        if (self.board[0,2] == player) and (self.board[1,1] == player) and (self.board[2,0] == player):
             self.current_winner = player


class Player():
    
    def __init__(self, player):
        self.player = player #x or o
    
    # return the square chose by human player wether valid
    def human_move(self, available_moves):
        valid_square = False
        square = None
        while not valid_square:
            inp = input(self.player + '\'s turn. Input move (0-8): ')
            try:
                square = int(inp)
                if square not in available_moves:
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again')
        return square
    
    # choose a random valid square for computer player
    def computer_move(self, available_moves):
        square = random.choice(available_moves)
        return square

# init function
def tictactoe(game, h_player, c_player):
    
    # in each round, we will be printing the game board and the numbers board
    game.print_board_num()
    game.print_board()
    
    player = 'human' # choosing human as firt move
    
    while not game.is_full():
        if player == 'human':
            square = h_player.human_move(game.available_moves()[0])
            game.players_move(square, h_player.player)
            game.winner(h_player.player)
        if player == 'computer':
            square = c_player.computer_move(game.available_moves()[0])
            game.players_move(square, c_player.player)
            game.winner(c_player.player)
            
        game.print_board_num()
            
        print(f'{player} makes a move to square {square}')
        game.print_board()
        print('')
        
        # in case of winner
        if game.current_winner:
            print(game.current_winner + ' wins!!')
            break
        
        # switching player
        player = 'computer' if player == 'human' else 'human'
        
        time.sleep(1)
    
    # in case of a tie
    if game.is_full() and not game.current_winner:
        print('it\'s a tie')



if __name__ == '__main__':
    game = Game()
    h_player = Player('x')
    c_player = Player('0')
    tictactoe(game, h_player, c_player)




















