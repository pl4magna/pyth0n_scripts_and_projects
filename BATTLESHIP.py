#!/usr/bin/env python3

'''

** Battleship game with python. **

'''

import random
import time

class Game:
    
    def __init__(self, player, winner=False):
        self.player = player
        self.winner = winner
        
    def declare_winner(self, grid):
        grid = [x for k in grid for x in k]
        if 'XX ' not in grid:
           print(f'{self.player} wins!!')
           self.winner = True
        else:
           pass
    
    # choose a random index for computer's move
    def computer_move(self):
        move = random.choice(range(49))
        return int(move)
    
    # return the human move
    def human_move(self):
        valid_square = False
        while not valid_square:
            try:
                move = int(input(self.player + '\'s turn. Input move (0-48): '))
                if move not in range(49):
                    raise ValueError
                valid_square = True                    
            except ValueError:
                print('please choose a number between 0 and 48...')
        return int(move)
    
    '''
    This method constructs a 1 dimensional grid for both human and computer player by inserting ships randomly. Since it just
    assigns a ship box casually, it could happened the choice of a previous square leading to an overlap of ships. To
    avoid that, it continuously finds new arrangement until the sum of each ship's box is equal to 12 (total of 4 ships
    composed by 3 boxes each).
    
    '''
    
    def ships(self):
        while True:
            grid = []          
            ships = []
            
            # horizontal ships
            o_box_generator = [val for val in (*range(3), *range(7,10), *range(14,17), *range(21,24), *range(28,31), *range(35,38), *range(42,45))]
            
            # vertical ships
            v_box_generator = [val for val in range(34)]
                   
            for o in range(2):
                box = random.choice(o_box_generator)
                o_ship = [box, box+1, box+2]
                ships.append(o_ship)                
                
            for v in range(2):
                box = random.choice(v_box_generator)
                v_ship = [box, box+7, box+14]
                ships.append(v_ship)
                
            fleet = [s for ship in ships for s in ship]
            if len(set(fleet)) < 12:
                continue
            grid = [['XX ' if i in fleet else '~~ ' for i in range(j*7, (j+1)*7)] for j in range(7)]
          
            break
        return grid

# upload human or computer grids after a move
def move(grid, square):
    # transform a nested list to a 1d list
    grid = [x for k in grid for x in k]
        
    if grid[square]=='XX ':
        grid.pop(square)
        grid.insert(square, '## ')
    if grid[square]=='~~ ':
        grid.pop(square)
        grid.insert(square, '00 ')
     
    grid= [grid[:7], grid[7:14], grid[14:21], grid[21:28], grid[28:35], grid[35:42], grid[42:49]]
    return grid

# this grid will be printed out masking the computer fleet (XX masked by ~~)
def censured_grid(c_grid, square):
    c_grid = [x for k in c_grid for x in k]
    c_grid = ['~~ ' if x=='XX ' else x for x in c_grid ]
            
    c_grid= [c_grid[:7], c_grid[7:14], c_grid[14:21], c_grid[21:28], c_grid[28:35], c_grid[35:42], c_grid[42:49]]
    return c_grid  

# print a 1d list (Game.ships()) as a 2d board. If num=True, a number board will be printed next to the player grid as well
def print_grid(ls, num=False):    
    board = '00,01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48'
    board = board.split(',')
    ls_ = ls.copy()
   
    if num:
        m=1
        for j in range(7):
            ls_.insert(m, board[(j*7):(j*7+7)])
            m += 2
            j += 7
        ls_ = [ls_[0]+ls_[1], ls_[2]+ls_[3], ls_[4]+ls_[5], ls_[6]+ls_[7], ls_[8]+ls_[9], ls_[10]+ls_[11], ls_[12]+ls_[13]]
 
        for row in ls_:
            print('| ' + ' | '.join(row) + ' |')
        print('----------------------')
            
    else:
        for row in ls:
            print('| ' + ' | '.join(row) + ' |')
        
 
# initialization
def play():
    human_player = Game('human')
    computer_player = Game('computer')
    h_grid = human_player.ships()
    c_grid = computer_player.ships()
    letter = 'h'
    h_moves = []
    c_moves = []
    
    print_grid(h_grid , num=True)
    square = human_player.human_move()
    h_moves.append(square)
    computer_grid = move(c_grid, square)
    print_grid(censured_grid(computer_grid, square), num=True)
    
    square = computer_player.computer_move()
    c_moves.append(square)
    human_grid = move(h_grid, square)
    print_grid(human_grid)
    time.sleep(0.7)
    
    while not human_player.winner and not computer_player.winner:
        
        human_player.declare_winner(computer_grid)
        computer_player.declare_winner(human_grid)
                
        if letter == 'h':
            
            t = True
            while t:
                square = human_player.human_move()
                try:
                    if square in h_moves:
                        raise ValueError
                    h_moves.append(square)
                    computer_grid = move(computer_grid, square)
                    print_grid(censured_grid(computer_grid, square), num=True)
                    time.sleep(0.7)                    
                    t = False
                except ValueError:
                    print('Already choosen. Try again..')
            
        else:
            while True:
                square = computer_player.computer_move()
                if square not in c_moves:
                    c_moves.append(square)
                    human_grid = move(human_grid, square)
                    print_grid(human_grid)
                    time.sleep(0.7)
                    break
                else:
                    continue
         
        letter = 'c' if letter == 'h' else 'h' 

header  = '''
\u001b[32m ______   _______ __________________ _        _______  _______          _________ _______ 
\u001b[32m(  ___ \ (  ___  )\__   __/\__   __/( \      (  ____ \(  ____ \|\     /|\__   __/(  ____ )
\u001b[32m| (   ) )| (   ) |   ) (      ) (   | (      | (    \/| (    \/| )   ( |   ) (   | (    )|
\u001b[32m| (__/ / | (___) |   | |      | |   | |      | (__    | (_____ | (___) |   | |   | (____)|
\u001b[32m|  __ (  |  ___  |   | |      | |   | |      |  __)   (_____  )|  ___  |   | |   |  _____)
\u001b[32m  (  \ \ | (   ) |   | |      | |   | |      | (            ) || (   ) |   | |   | (      
\u001b[32m| )___) )| )   ( |   | |      | |   | (____/\| (____/\/\____) || )   ( |___) (___| )      
\u001b[32m|/ \___/ |/     \|   )_(      )_(   (_______/(_______/\_______)|/     \|\_______/|/       

                                        \u001b[31mby____  ___  ___  ___     , \u001b[0m
                                        \u001b[31m' )  ) /  ` /  ) / ')' \ / \u001b[0m 
                                         \u001b[31m/--' /--  /  / /  /    X \u001b[0m  
                                        \u001b[31m/  \_(___,/__/_(__/    / \_\u001b[0m

\u001b[44m\u001b[37m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\u001b[0m
\u001b[44m\u001b[37m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\u001b[0m
\u001b[44m\u001b[37m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\u001b[47m\u001b[0m 
'''

legend = '''
Choose a number between 0 and 48.
XX --> your square ships
00 --> water
## --> hitten square ship
'''

print(header)  
print(legend)
play()
        


        
    
    
 
    
 

    
