from lib2to3.pgen2.token import COLON
import numpy as np
import pygame
import sys
import math

# Variables --------------------------------------------------------------------------------------------------------------------
ROW_COUNT = 6                       # Static variables are usually capitalized, to show that they are not changable
COLUMN_COUNT = 7
GRID_COLOR = (3,75,97)
PLAYER_ONE_COLOR = (188,95,106)
PLAYER_TWO_COLOR = (25, 179, 177)
WHITE = (255,255,255)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

width = COLUMN_COUNT*SQUARESIZE
height = (ROW_COUNT+1)*SQUARESIZE    # +1 row on top
size=(width, height)                 # type = tupel
game_over = False
turn = 0

# Functions --------------------------------------------------------------------------------------------------------------------
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))         # creates matrix with 6 columns and 7 rows, filled with '0'
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0                 # if the top row for the selected column is empty, the location is valid

# r counts up the rows, function gives back first row where passed column == 0
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:      
            return r

#check all horizontals, verticals, diagonals for winning combination
def winning_move(board, piece):
    # check horizontal location for win
    for c in range(COLUMN_COUNT-3):                     # -3 because a horizontal winning-combination cannot start in the last 3 columns
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board [r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check vertical location for win
    for c in range(COLUMN_COUNT):             
        for r in range(ROW_COUNT-3):                    # -3 because a vertical winning-combination cannot start in the last 3 rows
            if board[r][c]==piece and board [r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # check positivly sloped diagonals location for win
    for c in range(COLUMN_COUNT-3):            
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board [r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # check negativly sloped diagonals location for win
    for c in range(COLUMN_COUNT-3):             
        for r in range(3, ROW_COUNT):
            if board[r][c]==piece and board [r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# prints fliped board, so pieces fill up from the bottom (not the top)
def print_board(board):
    print(np.flip(board, 0))                            # flips board on axis '0' (= x-axis / Abszisse)

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range (ROW_COUNT):
            # Rectangle = surface, color, rect (= position width, position height, size width, size height) => https://www.pygame.org/docs/ref/draw.html
            pygame.draw.rect(screen, GRID_COLOR, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            # Circle = surface, color, position, radius => https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle
            pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range (ROW_COUNT):           
            if board[r][c] == 1:
                pygame.draw.circle(screen, PLAYER_ONE_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, PLAYER_TWO_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# Game --------------------------------------------------------------------------------------------------------------------
board = create_board()

pygame.init() # initializing pygame (has to be done in every pygame-project)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont('Monospace', 75)

while not game_over:

    # all events: https://www.pygame.org/docs/ref/event.html
    for event in pygame.event.get():            # pygame is an event-based library
        if event.type == pygame.QUIT:           # if x (top right corner) is clicked => exit game/ close window
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0,0,width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, PLAYER_ONE_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
                current_color = PLAYER_ONE_COLOR
            else:
                pygame.draw.circle(screen, PLAYER_TWO_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
                current_color = PLAYER_TWO_COLOR
            pygame.display.update()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, WHITE, (0,0,width, SQUARESIZE))
            # choose player
            if turn == 0:
                player = 1
            else:
                player = 2

            # ask player for input
            posx = event.pos[0]
            col = int(math.floor(posx/SQUARESIZE)) # "floor" rounds number down to nearest integer

            # play turn
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, player)

                # check for winning move
                if winning_move(board, player):
                    label = myfont.render(f"Player {player} Wins!",1,current_color) # 1 for axis (?)
                    screen.blit(label, (40,10)) # screen.blit draws one image onto another
                    game_over = True

            print_board(board)
            draw_board(board)

            # switch turn
            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3500)