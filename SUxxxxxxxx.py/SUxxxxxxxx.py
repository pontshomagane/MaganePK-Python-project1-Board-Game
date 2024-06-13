"""
Skeleton code for CS114 project 2024: A 3D board game.

This skeleton code for the project is intended as a starting point for students
to get an idea of how they can begin to code the project. You are not required
to use any of the functions in this skeleton code, however you may find some of
the ideas useful. You are however required to have the line:

if __name__ == "__main__":

but you are free to and should modify the lines following this.

None of the functions are implemented yet, so if you would like to
use a particular function, you need to implement it yourself. If you decide not
to use any of the functions, you are free to leave them empty or remove them
from this file. You are also free to alter the function signatures (the name of
the function and its arguments), so if you need to pass more arguments to the
function, or do not need a particular argument, you are also free to add and
remove arguments as you see fit. We provide the function signatures only as a
guide for how we think you can start to approach the project.
"""

# imports
import sys
import stdio
# Your imports go here


# global variables
count = 0;
# Your global variables go here
light_sinked_pieces = 0
dark_sinked_pieces = 0


def check_sink_range(row_max, col_max, row, col):
    """
    Function to check whether a sink is in the correct position.

    Args:
        row_max (int): The number of rows in the board
        col_max (int): The number of columns in the board
        row (int): The row of the sink
        col (int): The column of the sink

    Returns:
        bool: True if the sink is in the correct range, False otherwise.
    """
    if (col >= 0 and col < col_max ) and (row >= 0  and row<= col_max ):
        if (row < 3 or row >= row_max - 3) or (col < 3 and col >= col_max-3):
            return True

    return False

def check_piece_range(row_max, col_max, row, col):
    """
    Function to check whether a piece is in the correct position.

    Args:
        row_max (int): The number of rows in the board
        col_max (int): The number of columns in the board
        row (int): The row of the piece
        col (int): The column of the piece

    Returns:
        bool: True if the piece is in the correct range, False otherwise.
    """
    if (row  >= 0 and row < row_max) and (col >= 0 and col < col_max):
        if (row >= 3 and row < row_max - 3) and (col >= 3 and col < col_max - 3):
            return True
    return False


def check_piece_upright(row, col, board):
    """
    Function to check whether a piece is upright, or whether it is lying on it's
    side.

    Args:
        row (int): The row of the piece
        col (int): The column of the piece
        board (2D array of str): The game board

    Returns:
        bool: True if the piece is upright, False otherwise.
    """
    piece = board[row][col]

    upright = False
    # check the boards pieces using the coordinates
    # make sure the coordinates correspond to the occupied ones
    if piece in ['a','A','b','B','c','C']:
        if piece == 'a' or piece == 'A':
            upright = True

        elif piece != 'a' or piece != 'A':
            if board[row + 1][col] != ' ' and board[row][col + 1] != ' ':
                identifier = row * len(board[0]) + col
                if board[row + 1][col] == str(identifier) or board[row][col + 1] == str(identifier):
                    upright = False
                else:
                    upright = True
            else :
                upright = True

    # This function may be useful when determining how a piece is intended or
    # allowed to move.
    return upright


def get_piece_fields(row, col, board):
    """
    Get all the coordinates belonging to the piece at coordinate (row, col).

    Args:
        row (int): The row of the piece
        col (int): The column of the piece
        board (2D array of str): The game board

    Returns:
        array of coordinates: The fields that the piece occupies
    """
    piece = board[row][col]
    piece_fields = []

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == piece:
                piece_fields.append((i, j))

    return piece_fields

def validate_move(row, col, direction, board):
    """
    Checks whether the given move is valid by checking that all aspects of the
    move are legal.

    Args:
        row (int): The row of the object to move
        col (int): The column of the object to move
        direction (str): The direction of the move
        board (2D array of str): The game board

    Returns:
        bool: True if the move is valid, False otherwise
    """
    # Check if row and col are within the board
    if (row >= 0 and row < len(board)) and (col >= 0 and col < len(board[0])):
            # Check if the piece at (row, col) is a valid piece on the board
            piece = board[row][col]
            if piece != ' ':
                if direction in ['l', 'r', 'u', 'd', 'b', 'f'] :
                    if direction == 'r':
                        if validate_rightwards_move(row, col, piece, board) == False:
                            sys.exit(0)
                    elif direction == 'l':
                        if validate_leftwards_move(row, col, piece, board) == False:
                            sys.exit(0)
                    elif direction == 'u':
                        if validate_upwards_move(row, col, piece, board) == False:
                            sys.exit(0)
                    elif direction == 'd':
                        if validate_downwards_move(row, col,piece, board) == False:
                            sys.exit(0)
                    else:
                        stdio.writeln("NOTICE: Functionality not yet implemented")
                else:
                    stdio.writeln("ERROR: Invalid direction")
                    return False
            else:
                stdio.writeln(f"ERROR: No piece on field {row} {col}")
                return False

    else:
        stdio.writeln(f"ERROR: Field {row} {col} not on board")
        return False

def do_move(row, col, direction, board, scores, gui_mode):
    """
    Executes the given move on the board.

    Args:
        row (int): The row of the object to move
        col (int): The column of the object to move
        direction (str): The direction of the move
        board (2D array of str): The game board
        scores (array of int): The current scores for each player
        gui_mode (bool): The mode of the game, True if gui_mode, False if terminal mode
    """
    # This function may be useful for separating out the logic of doing a move.

    if direction == 'l':
        move_left_right(row, col, direction, board)
        print_board(board)
        stdio.writeln()

    elif direction == 'r':
        move_left_right(row, col, direction, board)
        print_board(board)
        stdio.writeln()

    elif direction == 'u':
        move_up_down(row, col, direction, board)
        print_board(board)
        stdio.writeln()

    else :
        move_up_down(row, col, direction, board)
        field_for_bottom_left_most(len(board), len(board[0]), board)
        print_board(board)
        stdio.writeln()





#-------------------- Newly Moving added Functions ----------------------------#
def validate_downwards_move(row, col, piece, board):
    """
    Validates a downwards move for a given piece on the board.

    Args:
        row (int): The current row of the piece.
        col (int): The current column of the piece.
        piece (str): The piece to be moved.
        board (list): The game board.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if piece == 'a' or 'A':
        if row - 1 >= 0:
            if board[row - 1][col] == ' ':
                return True
            else:
                row = row -1
                stdio.writeln(f"ERROR: Field {row} {col} not free")
                return False
        else:
            stdio.writeln("ERROR: Cannot move beyond the board")
            return False
    elif piece == 'b' or piece == 'B':
        if check_piece_upright(row, col, board):
            if row - 2 >= 0:
                if board[row - 1][col] == ' ' and board[row - 2][col] == ' ':
                    return True
                else:
                    row = row -2
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
        else:
            if row - 1 >= 0:
                if board[row - 1][col] == ' ':
                    return True
                else:
                    row = row -1
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
    elif piece == 'c' or piece == 'C':
        if check_piece_upright(row, col, board):
            if row - 3 >= 0:
                if board[row - 1][col] == ' ' and board[row - 2][col] == ' ' and board[row - 3][col] == ' ':
                    return True
                else:
                    row = row-3
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
        else:
            if row - 1 >= 0:
                if board[row - 1][col] == ' ':
                    return True
                else:
                    row= row - 1
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
def validate_upwards_move(row, col, piece, board):
    """
    Validates an upwards move for a given piece on the board.

    Args:
        row (int): The row index of the piece on the board.
        col (int): The column index of the piece on the board.
        piece (str): The type of piece ('a', 'b', 'c', or any other character).
        board (list): The game board represented as a 2D list.

    Returns:
        bool: True if the move is valid, False otherwise.

    Raises:
        None

    """
    if piece == 'a' or 'A':
        if row + 1 < len(board):
            if board[row + 1][col] == ' ':
                return True
            else:
                stdio.writeln(f"ERROR: Field {row} {col} not free")
                return False
        else:
            stdio.writeln("ERROR: Cannot move beyond the board")
            return False
    elif piece == 'b' or piece == 'B':
        if check_piece_upright(row, col, board):
            if row + 1 < len(board) and row + 2 < len(board):
                if board[row + 1][col] == ' ' and board[row + 2][col] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
        else:
            if row + 1 < len(board):
                if board[row + 1][col] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
    elif piece == 'c' or piece == 'C':
        if check_piece_upright(row, col, board):
            if (row + 1 < len(board) and row + 2 < len(board)) and row + 3 < len(board):
                if board[row + 1][col] == ' ' and board[row+ 2][col] == ' ' and board[row +2][col] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return True
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
        else:
            if row + 1 < len(board):
                if board[row + 1] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False

def validate_leftwards_move(row, col, piece, board):
    """
    Validates a leftwards move for a given piece on the board.

    Args:
        row (int): The row index of the piece on the board.
        col (int): The column index of the piece on the board.
        piece (str): The piece to be moved.
        board (list): The game board.

    Returns:
        bool: True if the move is valid, False otherwise.

    Raises:
        None

    """
    if piece == 'a' or 'A':
        if col - 1 >= 0:
            if board[row][col - 1] == ' ':
                return True
            else:
                stdio.writeln(f"ERROR: Field {row} {col} not free")
                return False
        else:
            stdio.writeln("ERROR: Cannot move beyond the board")
            return False
    elif piece == 'b' or piece == 'B':
        if check_piece_upright(row, col, board):
            if col - 1 >= 0 and col - 2 >= 0:
                if board[row][col - 1] == ' ' and board[row][col - 2] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
        else:
            if col - 1 >= 0:
                if board[row][col - 1] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
    elif piece == 'c' or piece == 'C':
        if check_piece_upright(row, col, board):
            if col - 1 >= 0 and col - 2 >= 0 and col - 3 >= 0:
                if board[row][col - 1] == ' ' and board[row][col - 2] == ' ' and board[row][col -3] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
        else:
            if col - 1 >= 0:
                if board[row][col -1] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False

def validate_rightwards_move(row, col, piece, board):
    """
    Validates a rightwards move for a given piece on the board.

    Args:
        row (int): The row index of the piece on the board.
        col (int): The column index of the piece on the board.
        piece (str): The type of piece being moved.
        board (list): The game board represented as a 2D list.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if piece == 'a' or 'A':
        if col + 1 < len(board[0]):
            if board[row][col + 1] == ' ':
                return True
            else:
                stdio.writeln(f"ERROR: Field {row} {col} not free")
                return False
        else:
            stdio.writeln("ERROR: Cannot move beyond the board")
            return False
    elif piece == 'b' or 'B':
        if check_piece_upright(row, col, board):
            if col + 1 < len(board[0]) and col + 2 < len(board[0]):
                if board[row][col + 1] == ' ' and board[row][col + 2] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
        else:
            if col + 1 < len(board[0]):
                if board[row][col + 1] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
    elif piece == 'c' or piece == 'C':
        if check_piece_upright(row, col, board):
            if col + 1 < len(board[0]) and col + 2 < len(board[0]) and col + 3 < len(board[0]):
                if (board[row][col + 1] == ' ' and board[row][col + 2] == ' ' )and board[row][col + 3] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False
        else:
            if col + 1 < len(board[0]):
                if board[row][col + 1] == ' ':
                    return True
                else:
                    stdio.writeln(f"ERROR: Field {row} {col} not free")
                    return False
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                return False


def move_left_right(row, col, direction, board):
    piece = board[row][col]

    if piece == 'a' or piece == 'A':
        if direction == 'r':
            board[row][col] = ' '
            board[row][col + 1] = piece
        else:
            board[row][col] = ' '
            board[row][col - 1] = piece

    elif piece == 'd' or piece == 'D':
        board[row][col] = ' '
        board[row][col + 1] = ' '
        board[row + 1][col] = ' '
        board[row + 1][col + 1] = ' '

        if direction == 'r':
           identifier = row * len(board[0]) + (col + 2)
           board[row + 1][col + 2] = str(identifier)
           board[row ][col + 2] = piece
           board[row ][col + 3] =str(identifier)
           board[row + 1][col+ 3] = str(identifier)
        else:
           identifier = row * len(board[0]) + (col -2)
           board[row + 1][col - 2] = str(identifier)
           board[row ][col - 2] = piece
           board[row ][col -1] =str(identifier)
           board[row + 1][col-1] = str(identifier)

    elif piece == 'b' or piece == 'B':
        curr_id = row * len(board[0]) + col

        if direction == 'r':
            identifier = row * len(board[0]) + (col+1)
            if board[row][col + 1] == curr_id:
                board[row][col] = ' '
                board[row][col + 1] = piece

            elif board[row+1][col] == curr_id:
                board[row+1][col] = ' '
                board[row][col] = ' '

                board[row][col+ 1] = piece
                board[row+1][col+ 1] = str(identifier)
            else:
                board[row][col] = ' '

                board[row][col+ 1] = piece
                board[row][col+ 2] = str(identifier)
        else:
            if board[row][col + 1] == curr_id:
                board[row][col + 1] = ' '

                board[row][col] = piece

            elif board[row+1][col] == curr_id:
                identifier = row * len(board[0]) + (col-1)
                board[row+1][col] = ' '
                board[row][col] = ' '
                board[row][col-1] = piece
                board[row-1][col-1] = str(identifier)
            else:
                identifier = row * len(board[0]) + (col-1)
                board[row][col] = ' '
                board[row][col-1] = piece
                board[row][col-2] = str(identifier)


    elif piece == 'c' or piece == 'C':
        curr_id = row * len(board[0]) + col


        if direction == 'r':
            identifier = row * len(board[0]) + (col+1)
            if board[row][col + 1] == curr_id:
                board[row][col + 1] = ' '
                board[row][col + 2] = ' '
                board[row][col + 3] = piece

            elif board[row+1][col] == curr_id:
                board[row+1][col] = ' '
                board[row+2][col] = ' '
                board[row][col+1] = piece
                board[row+1][col+1] = str(identifier)
                board[row+2][col+1] = str(identifier)
            else:
                board[row][col+ 1] = piece
                board[row][col+ 2] = str(identifier)
                board[row][col+ 3] = str(identifier)
        else:
            identifier = row * len(board[0]) + (col-1)
            if board[row][col + 1] == curr_id:
                board[row][col + 1] = ' '
                board[row][col + 2] = ' '
                board[row][col-1] = piece

            elif board[row+1][col] == curr_id:
                board[row+1][col] = ' '
                board[row+2][col] = ' '

                board[row][col-1] = piece
                board[row+1][col-1] = str(identifier)
                board[row+2][col-1] = str(identifier)
            else:
                identifier = row * len(board[0]) + (col-3)
                board[row][col] = ' '
                board[row][col-1] = str(identifier)
                board[row][col-2] = str(identifier)
                board[row][col-3] = piece

    # remove the following line when you add something to this function:
    pass

def move_up_down(row, col, direction, board):
    piece = board[row][col]

    if piece == 'a' or piece == 'A':
        board[row][col] = ' '
        board[row + 1][col] = piece
    elif piece == 'd' or piece == 'D':

        if direction == 'u':
            identifier = (row +2) * len(board[0]) + col
            board[row][col] = ' '
            board[row][col + 1] = ' '
            board[row + 1][col] = ' '
            board[row + 1][col + 1] = ' '

            board[row + 2][col] = piece
            board[row + 2][col + 1] = str(identifier)
            board[row + 3][col] =str(identifier)
            board[row + 3][col+ 1] = str(identifier)
        else:
            identifier = (row - 2) * len(board[0]) + col
            board[row][col] = ' '
            board[row][col + 1] = ' '
            board[row + 1][col] = ' '
            board[row + 1][col + 1] = ' '

            board[row - 2][col] = piece
            board[row - 1][col] = str(identifier)
            board[row - 1][col + 1] = str(identifier)
            board[row - 2][col + 1] = str(identifier)

    elif piece == 'b' or piece == 'B':
        curr_id = row * len(board[0]) + col

        if direction == 'u':
            if board[row][col + 1] == curr_id:
                identifier = (row +1) * len(board[0]) + col
                board[row][col + 1] = ' '
                board[row][col] = ' '

                board[row + 1][col] = piece
                board[row + 1][col + 1] = str(identifier)
            elif board[row+1][col] == curr_id:
                identifier = (row + 2) * len(board[0]) + col
                board[row][col] = ' '
                board[row + 1][col] = ' '

                board[row + 2][col] = piece
            else:
                identifier = (row + 2) * len(board[0]) + col
                board[row][col] = ' '
                board[row + 1][col] = piece
                board[row + 2][col] = str(identifier)
        else:
            if board[row][col + 1] == curr_id:
                identifier = (row - 1) * len(board[0]) + col
                board[row][col + 1] = ' '
                board[row][col] = ' '

                board[row - 1][col] = piece
                board[row - 1][col + 1] = str(identifier)
            elif board[row+1][col] == curr_id:
                identifier = (row - 2) * len(board[0]) + col
                board[row][col] = ' '
                board[row + 1][col] = ' '

                board[row - 1][col] = piece
            else:
                identifier = (row - 2) * len(board[0]) + col
                board[row][col] = ' '
                board[row - 1][col] = str(identifier)
                board[row - 2][col] = piece

    elif piece == 'c' or piece == 'C':
        curr_id = row * len(board[0]) + col

        if direction == 'u':
            identifier = (row + 1) * len(board[0]) + col
            if board[row][col + 1] == curr_id:
                board[row][col + 1] = ' '
                board[row][col + 2] = ' '
                board[row][col] = ' '

                board[row + 1][col] = piece
                board[row + 1][col +1] = str(identifier)
                board[row + 1][col + 2] = str(identifier)

            elif board[row+1][col] == curr_id:
                board[row + 1][col] = ' '
                board[row + 2][col] = ' '
                board[row][col] = ' '

                board[row + 3][col] = piece
            else:
                board[row][col] = ' '
                board[row + 1][col] = piece
                board[row + 2][col] = str(identifier)
                board[row + 3][col] = str(identifier)
        else:
            identifier = (row - 1) * len(board[0]) + col
            if board[row][col + 1] == curr_id:
                board[row][col + 1] = ' '
                board[row][col + 2] = ' '
                board[row][col] = ' '

                board[row - 1][col] = piece
                board[row - 1][col +1] = str(identifier)
                board[row - 1][col + 2] = str(identifier)

            elif board[row+1][col] == curr_id:
                board[row + 1][col] = ' '
                board[row + 2][col] = ' '
                board[row][col] = ' '

                board[row - 1][col] = piece
            else:
                identifier = (row - 3) * len(board[0]) + col
                board[row][col] = ' '
                board[row - 1][col] = str(identifier)
                board[row - 2][col] = str(identifier)
                board[row - 3][col] = piece
    field_for_bottom_left_most(len(board), len(board[0]), board)




def generate_all_moves(board):
    """
    Generates a list of all moves (valid or invalid) that could potentially be
    played on the current board.

    Args:
        board (2D array of str): The game board

    Returns:
        array of moves: The moves that could be played on the given board
    """
    # When used with the validate_move function, this function is useful for
    # checking whether a player has a valid move left to play.
    # remove the following line when you add something to this function:
    pass


def read_board(row_max, col_max):
    """
    This function reads in the board from stdin and constructs the board,
    returning this board when it is done.

    Args:
        row_max (int): The number of rows in the board
        col_max (int): The number of columns in the board

    Returns:
        2D array of str: The board that was constructed
    """
    # TODO: implement this function.
    # Initalize the board
    board = [[' ' for i in range(col_max)] for j in range(row_max)]

    # Read the from the stdin
    while True:
        #assumes the input is in correct format
        line = stdio.readLine()
        if line == '#':
            break

        boardInput = line.split()
        typeOfObject = boardInput[0]

        if typeOfObject == 'x':

            # need to check if the given coordinate is an integer

            row = int(boardInput[1])
            col = int(boardInput[2])
            validate_piece_coordinates
            if filed_on_board(row, col, board) :
                if row < 0 or row >= row_max or col < 0 or col >= col_max:
                    stdio.writeln(f"ERROR: Field {row} {col} not on board")
                    sys.exit(0)
                board[row][col] = 'x'

        elif typeOfObject == 's':
            pieceSize = int(boardInput[1])
            row = int(boardInput[2])
            col = int(boardInput[3])
            if filed_on_board(row, col, board) :
                validate_piece_coordinates(row, col, row_max, col_max)

                if not check_sink_range(row_max, col_max, row, col):
                    stdio.writeln("ERROR: Sink in the wrong position")
                    sys.exit(1)
                for i in range(row, row + pieceSize):
                    for j in range(col, col + pieceSize):
                        board[i][j] = 's'

        # The palyers' pieces
        elif typeOfObject in ['d', 'l']:
            pieceType = boardInput[1]
            row = int(boardInput[2])
            col = int(boardInput[3])
            if filed_on_board(row, col, board) :
                validate_piece_coordinates(row, col, row_max, col_max)

                if not check_piece_range(row_max, col_max, row, col):
                    stdio.writeln("ERROR: Piece in the wrong position")
                    sys.exit(1)
                if typeOfObject == 'd':
                    pieceUpperCase = pieceType.upper()
                    board[row][col] = pieceUpperCase

                else:
                    board[row][col] = pieceType
        else:
            stdio.writeln(f"ERROR: Invalid object type {typeOfObject}")
            sys.exit(0)
    # Traverse all cells in the board
    field_for_bottom_left_most(row_max, col_max, board)

    return board


def print_board(board):
    """
    Prints the given board out to the standard output in the format specified in
    the project specification.

    Args:
        board (2D array of str): The game board
    """
    # Print the column numbers
    stdio.write('    ' + '  '.join(str(i) for i in range(len(board[0]))))
    stdio.writeln()
    # Print the horizontal line
    stdio.write('  ' + '+--' * len(board[0]) + '+')
    stdio.writeln()

    # Print each row of the board
    for i in range(len(board) -1, -1, -1):
        # Print the row number and the cells of the row
        row = []
        for j in range(len(board[i])):
            cell = board[i][j]

            if is_identifier(board,  cell):  # identifier
                row += [ cell]

            elif cell == 's':  # Sink
                row += [' s']
            elif cell == 'x':  # Blocked field
                row += [' x']
            elif cell in ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']:  # Piece

                row += [' ' + cell]
            else:
                row += ['  ']

        stdio.write(str(i) + ' |' + '|'.join(row) + '|')
        stdio.writeln()
        # Print the horizontal line
        stdio.write('  ' + '+--' * len(board[0]) + '+')
        stdio.writeln()

def game_loop(board, gui_mode):
    """
    Executes the main game loop including
        * reading in a move
        * checking if the move is valid
        * if it is, doing the move
        * printing (or displaying) the board
        * and repeating.

    Args:
        board (2D array of str): The game board
        gui_mode (bool): The mode of the game, True if gui_mode, False if terminal mode
    """
    # If implemented well, this function can be used for both terminal and GUI mode.
    # TODO: implement this function.
    is_light_player = True # This line to keep track of whose turn it is
    move_count = 0 # This line to keep track of the number of moves

    while True:
        # Read the move from the stdin
        try:
            line = stdio.readLine()
        except EOFError:
            break

        if not line:
            print_board(board)
            stdio.writeln("patial game")
            sys.exit(0)

        # Parse a move
        move = line.split()
        row = int(move[0])
        col = int(move[1])
        action = move[2]

        scores =[light_sinked_pieces, dark_sinked_pieces]
        # Validate the move and do the move
        if is_light_player:
            # TODO: Validate the move and do the move for player 1
            if validate_move(row, col, action, board) == False:
                sys.exit(0)
            else:
                do_move(row, col, action, board, scores, gui_mode)
                # increment for lighter player
            pass
        else:
            # The it is thedarker player's turn
            # TO: Validate the move and do the move for player 2
            # increment for darker playODer
            pass

        # Increase the move count
        move_count += 1

        # Check if the player has made two moves or moved diagonally
        if move_count == 2 or action == 'd':
            # Switch turns
            is_light_player = not is_light_player
            move_count = 0  # Reset the move count

        # Check if the game is over
        if scores[0] == 4:
            stdio.writeln("Light wins!")
            sys.exit(0)
        elif scores[0] == 4:
            stdio.writeln("Dark wins!")
            sys.exit(0)
    # remove the following line when you add something to this function:


def validate_piece_coordinates(row, col, row_max, col_max):
    """
    Function that validates the coordinates of a piece.

    Args:
        row (int): The row of the piece
        col (int): The column of the piece
        row_max (int): The maximum number of rows
        col_max (int): The maximum number of columns
    """
    if not isinstance(row, int) or not isinstance(col, int):
        stdio.writeln(f"ERROR: Field {row} {col} not on board")
        sys.exit(0)

    if row < 0 or row >= row_max or col < 0 or col >= col_max:
        stdio.writeln(f"ERROR: Field {row} {col} not on board")
        sys.exit(0)

#-------------------- Newly added Functions ----------------------------#
# def win_loose(row, col, piece, direction board):
#     """_summary_

#     Args:
#         row (_type_): _description_
#         col (_type_): _description_
#         piece (_type_): _description_
#         board (_type_): _description_
#     """
#     count_darker = 0
#     count_lighter = 0
#     sink = 0
#     if piece == 'a' or 'A':
#         if board[row][col] == 's':
#             count_darker = count_darker + 1
#             count_lighter = count_lighter + 1

#     elif piece == 'b' or 'B':
#         if board[row][col] == 's':
#             if check_piece_upright(row, col, board) == False:
#                 if board[row][col-1] != ' ':
#                     count_darker = count_darker + 1
#                     count_lighter = count_lighter + 1

#     pass

def filed_on_board(row, col, board):
    """_summary_

    Args:
        row (_type_): _description_
        col (_type_): _description_
        board (_type_): _description_

    Returns:
        _type_: _description_
    """
    on_board = False
    if (row >= 0 and row < len(board) )and (col >= 0 and col  < len(board[0])):
        on_board = True
    else:
        stdio.writeln(f"ERROR: Field {row} {col} not on board")
        sys.exit(0)
    return on_board
def is_identifier(board,  cell):
    """
    Function to check if the cell is an identifier.
    Uses the formula : identifier = row * num_columns + col
    to calculate the identifier of a cell.

    Args:
        board (2D array of str): The game board
        cell (string): The cell to check if it is an identifier

    Returns:
        bool: True if the cell is an identifier, False otherwise.
    """
    num_rows = len(board)
    num_columns = len(board[0])

    # Initialize the identifiers array
    identifiers = [['' for _ in range(num_columns)] for _ in range(num_rows)]

    # Calculate and store identifiers for each cell
    for i in range(num_rows):
        for j in range(num_columns):
            identifier = str(i * num_columns + j)
            identifiers[i][j] = identifier

    for x, value in enumerate(identifiers):
        for y, val in enumerate(value):
            if val == cell:
                return True
    return False

def field_for_bottom_left_most(row_max, col_max, board):
    """
    Function to update the fields that the bottom left piece occupies.

    Args:
        row_max (int): The maximum number of rows
        col_max (int): The maximum number of columns
        board (2D array of str): The game board
    """
    for i in range(row_max):
        for j in range(col_max):
            # Check if the current cell has a piece
            if board[i][j] != ' ' and board[i][j] != 'x' and board[i][j] != 's':
                identifier = i * len(board[0]) + j
                cell_id = str(identifier)

                if (i < row_max- 1 and j < col_max -1) and board[i+1][j+1] == ' ':
                    # Check if the cell on the same row + 1 is empty
                    if i < row_max-1 and board[i+1][j] == ' ':
                        # Check if the cell on the same column + 1 is empty
                        if j < col_max-1 and board[i][j+1] == ' ':
                            board[i+1][j+1] = cell_id
                            board[i][j+1] = cell_id
                            board[i+1][j] = cell_id


if __name__ == "__main__":
    # TODO: put logic here to check if the command-line arguments are correct,

    # validating the number of arguments
    if (len(sys.argv) < 4):
        stdio.writeln("ERROR: Too few arguments")
        sys.exit(0)
    elif (len(sys.argv) > 4):
        stdio.writeln("ERROR: Too many arguments")
        sys.exit(0)

    # validation of the arguments
    try:
        height = int(sys.argv[1])
        width = int(sys.argv[2])
        mode = int(sys.argv[3])
        if height < 8 or height > 10:
            raise ValueError
        if width < 8 or width > 10:
            raise ValueError
        if mode != 0 and mode != 1:
            raise ValueError
    except ValueError:
        stdio.writeln("ERROR: Invalid argument")
        sys.exit(0)

    # and then call the game functions using these arguments. The following code
    # is a placeholder for this to give you an idea, and MUST be changed when
    # you start editing this file.
    board = read_board(height, width)
    print_board(board)
    game_loop(board, mode)
