import numpy as np

# Variables --------------------------------------------------------------------------------------------------------------------
ROW_COUNT = 6                       # Static variables are usually capitalized, to show that they are not changable
COLUMN_COUNT = 7

game_over = False
turn = 0

# Functions --------------------------------------------------------------------------------------------------------------------
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))         # creates matrix with 6 columns and 7 rows, filled with '0'
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0       # if the top row for the selected column is empty, the location is valid

# r counts up the rows, function gives back first row where passed column == 0
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:      
            return r

#check all horizontals, verticals, diagonals for winning combination
def winning_move(board, piece):
    # check horizontal location for win
    for c in range(COLUMN_COUNT-3):             # -3 because a horizontal winning-combination cannot start in the last 3 columns
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board [r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check vertical location for win
    for c in range(COLUMN_COUNT):             
        for r in range(ROW_COUNT-3):            # -3 because a vertical winning-combination cannot start in the last 3 rows
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
    print(np.flip(board, 0))                    # flips board on axis '0' (= x-axis / Abszisse)

# Game --------------------------------------------------------------------------------------------------------------------
board = create_board()

while not game_over:
    # choose player
    if turn == 0:
        player = 1
    else:
        player = 2

    # ask player for input
    col = int(input(f"Player {player} make your selection (0-6): "))

    # play turn
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)

    # print board
    print_board(board)

    # check for winning move
    if winning_move(board, player):
        print(f"Player {player} Wins!!! Congrats!!!")
        game_over = True
        break

    # switch turn
    turn += 1
    turn = turn % 2