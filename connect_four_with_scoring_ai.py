import numpy as np
import pygame
import sys
import math
import random

# Variables --------------------------------------------------------------------------------------------------------------------
ROW_COUNT = 6                       # Static variables are usually capitalized, to show that they are not changable
COLUMN_COUNT = 7
GRID_COLOR = (3,75,97)
PLAYER_ONE_COLOR = (188,95,106)
PLAYER_TWO_COLOR = (25, 179, 177)
WHITE = (255,255,255)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
#PLAYER = 0
#AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
EMPTY = 0

width = COLUMN_COUNT*SQUARESIZE
height = (ROW_COUNT+1)*SQUARESIZE    # +1 row on top
size=(width, height)                 # type = tupel
game_over = False
turn = random.randint(0,1)
print(turn)

# Functions --------------------------------------------------------------------------------------------------------------------
# creates board-object
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))         # creates matrix with 6 columns and 7 rows, filled with '0'
    return board

# puts piece at selected location
def drop_piece(board, row, col, piece):
    board[row][col] = piece

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
    for r in range(ROW_COUNT):
        if board[r][col] == 0:      
            return r

# check all horizontals, verticals, diagonals for winning combination
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

# Look at a window of 4 positions next to each other and count if 2,3,4 in a row
def score_position(board, piece):
    score = 0
    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    #for r in range(ROW_COUNT-3):
    #    window = center_array[r:r-WINDOW_LENGTH]
    #    score = (evaluate_window(window, piece))*3
    center_count = center_array.count(piece)
    score += center_count * 2
    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])] # array with row r & all column positions for that row
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    # Score positive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    # Score negative sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# returns score depending on how many pieces of same player are in a (otherwise empty) window of 4
def evaluate_window(window, piece):

    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    
    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1: # block opponent, if he/she has 3 in a row
        score -= 4

    return score

# evaluates and returns column with highest score (= best possible move)
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -1000 # negative number, so if score is negative (-4) it is still larger than this initialized best_score (-1000)
    best_col = random.choice(valid_locations)
    # simulate dropping piece in board and score position
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()  # need a copied board for simulation, because original board would use same memory location
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
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
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, PLAYER_ONE_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, PLAYER_TWO_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# Game --------------------------------------------------------------------------------------------------------------------
board = create_board()

pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont('Monospace', 75)

while not game_over:

    # all events: https://www.pygame.org/docs/ref/event.html
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           # if x (top right corner) is clicked => exit game/ close window
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, WHITE, (0,0,width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, PLAYER_ONE_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
                current_color = PLAYER_ONE_COLOR
            else:
                current_color = PLAYER_TWO_COLOR
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 wins!!", 1, PLAYER_ONE_COLOR)
                            screen.blit(label, (40,10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        # # Ask for Player 2 Input
        if turn == 1 and not game_over:
            col = pick_best_move(board, AI_PIECE)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 wins!!", 1, PLAYER_TWO_COLOR)
                    screen.blit(label, (40,10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3500)