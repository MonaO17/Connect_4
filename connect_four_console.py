import numpy as np

ROW_COUNT = 6                       # Static variables are usually capitalized, to show that they are not changable
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((6,7))         # creates matrix with 6 columns and 7 rows, filled with '0'
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[5][col] == 0       # if the top row for the selected column is empty, the location is valid

# r counts up the rows, function gives back first row where passed column == 0
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:      
            return r

# prints fliped board, so pieces fill up from the bottom (not the top)
def print_board(board):
    print(np.flip(board, 0))           # flips board on axis '0' (= x-axis / Abszisse)

board = create_board()
game_over = False
turn = 0

while not game_over:
    # choose player
    if turn == 0:
        player = 1
    else:
        player = 2

    # ask player for input
    col = int(input(f"Player {player} make your Selection (0-6): "))

    # play turn
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player)

    print_board(board)

    turn += 1
    turn = turn % 2