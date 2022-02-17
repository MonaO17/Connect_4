import numpy as np
import pygame
import sys
import math
import random

# Variables --------------------------------------------------------------------------------------------------------------------
ROW_COUNT = 6
COLUMN_COUNT = 7
GRID_COLOR = (3,75,97)
PLAYER_COLOR = (188,95,106)
AI_COLOR = (25, 179, 177)
WHITE = (255,255,255)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
WIDTH = COLUMN_COUNT*SQUARESIZE
HEIGHT = (ROW_COUNT+1)*SQUARESIZE
SIZE=(WIDTH, HEIGHT)

PLAYER = 1
AI = 2
PLAYER_TURN = 0
AI_TURN = 1

WINDOW_LENGTH = 4
EMPTY = 0
game_over = False
turn = random.randint(0,1)

# Functions --------------------------------------------------------------------------------------------------------------------
# creates board-object
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))         # creates matrix with 6 columns and 7 rows, filled with '0'
    return board

# check is selected location is available
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0                 # if the top row for the selected column is empty, the location is valid

# returns a list of valid locations
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# r counts up the rows, function gives back first row where passed column == 0
def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:      
            return row

# puts piece at selected location
def drop_piece(board, row, col, player):
    board[row][col] = player

# check all horizontals, verticals, diagonals for winning combination
def winning_move(board, player):
    # check horizontal location for win
    for c in range(COLUMN_COUNT-3):                     # -3 because a horizontal winning-combination cannot start in the last 3 columns
        for r in range(ROW_COUNT):
            if board[r][c] == player and board [r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True
    # check vertical location for win
    for c in range(COLUMN_COUNT):             
        for r in range(ROW_COUNT-3):                    # -3 because a vertical winning-combination cannot start in the last 3 rows
            if board[r][c] == player and board [r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True
    # check positivly sloped diagonals location for win
    for c in range(COLUMN_COUNT-3):            
        for r in range(ROW_COUNT-3):
            if board[r][c] == player and board [r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True
    # check negativly sloped diagonals location for win
    for c in range(COLUMN_COUNT-3):             
        for r in range(3, ROW_COUNT):
            if board[r][c] == player and board [r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

# Splits board in windows of 4 coherent positions and evaluates them, returns score
def score_position(temp_board, player):
    score = 0
    # Score center column
    center_array = [int(i) for i in list(temp_board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(player)
    score += center_count * 2
    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(temp_board[r,:])] # array with row r & all column positions for that row
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, player)
    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(temp_board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, player)
    # Score positive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [temp_board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, player)
    # Score negative sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [temp_board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, player)

    return score

# returns score depending on how many pieces of same player are in a (otherwise empty) window of 4
def evaluate_window(window, player):
    score = 0
    opp_player = PLAYER
    if player == PLAYER:
        opp_player = AI
    
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_player) == 3 and window.count(EMPTY) == 1: # block opponent, if he/she has 3 in a row
        score -= 6

    return score

# evaluates and returns column with highest score (= best possible move)
def pick_best_move(board, player):
    valid_locations = get_valid_locations(board)
    best_score = -100 # negative number, so if score is negative (-4) it is still larger than this initialized best_score (-1000)
    best_col = random.choice(valid_locations)
    # simulate dropping piece in board and score position
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()  # need a copied board for simulation, because original board would use same memory location
        drop_piece(temp_board, row, col, player)
        score = score_position(temp_board, player)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

# prints fliped board, so pieces fill up from the bottom (not the top)
def print_board(board):
    print(np.flip(board, 0))                            # flips board on axis '0' (= x-axis / Abszisse)

# draws graphical connect-four board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range (ROW_COUNT):
            # Rectangle = surface, color, rect (= position width, position height, size width, size height) => https://www.pygame.org/docs/ref/draw.html
            pygame.draw.rect(screen, GRID_COLOR, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            # Circle = surface, color, position, radius => https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle
            pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range (ROW_COUNT):           
            if board[r][c] == PLAYER:
                pygame.draw.circle(screen, PLAYER_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI:
                pygame.draw.circle(screen, AI_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# Game --------------------------------------------------------------------------------------------------------------------
board = create_board()

pygame.init()
screen = pygame.display.set_mode(SIZE)
myfont = pygame.font.SysFont('Monospace', 75)
draw_board(board)

while not game_over:

    for event in pygame.event.get():            # all events: https://www.pygame.org/docs/ref/event.html
        if event.type == pygame.QUIT:           # if x (top right corner) is clicked => exit game/ close window
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0,0,WIDTH,SQUARESIZE))
            #print(event.pos)
            posx = event.pos[0]
            if turn == PLAYER_TURN:
                pygame.draw.circle(screen, PLAYER_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN or turn == AI_TURN:
            pygame.draw.rect(screen, WHITE, (0,0,WIDTH, SQUARESIZE))
            # choose player & set variables
            if turn == PLAYER_TURN:
                player = PLAYER
                current_color = PLAYER_COLOR
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE)) # "floor" rounds number down to nearest integer
            else:
                player = AI
                current_color = AI_COLOR
                pygame.time.wait(500)
                col = pick_best_move(board, AI)
                
            # play turn
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, player)

                # check for winning move
                if winning_move(board, player):
                    label = myfont.render(f"Player {player} Wins!",1,current_color) # 1 for axis (?)
                    screen.blit(label, (40,10)) # screen.blit draws one image onto another
                    game_over = True

            # switch turn
            turn = (turn+1) % 2

            print_board(board)
            draw_board(board)

        if game_over:
            pygame.time.wait(3500)