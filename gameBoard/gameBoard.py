#!/usr/bin/env python3
"""
Unified Board Game Implementation
Usage: python game.py <height> <width> <mode>
Where mode: 0 = text mode, 1 = GUI mode
"""

import sys
import stdio
import tkinter as tk
from tkinter import messagebox


class GameState:
    """Manages the game state and rules"""
    
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[' ' for _ in range(width)] for _ in range(height)]
        self.light_sinked_pieces = 0
        self.dark_sinked_pieces = 0
        self.current_player = 'light'  # 'light' or 'dark'
        self.move_count = 0
        
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.light_sinked_pieces = 0
        self.dark_sinked_pieces = 0
        self.current_player = 'light'
        self.move_count = 0
        
    def switch_player(self):
        """Switch to the other player"""
        self.current_player = 'dark' if self.current_player == 'light' else 'light'
    
    def check_win_condition(self):
        """Check if someone has won"""
        if self.light_sinked_pieces >= 4:
            return 'light'
        elif self.dark_sinked_pieces >= 4:
            return 'dark'
        return None


class Piece:
    """Represents a game piece with its properties and behavior"""
    
    PIECE_TYPES = {
        'a': {'name': 'small', 'size': 1, 'team': 'light'},
        'A': {'name': 'small', 'size': 1, 'team': 'dark'},
        'b': {'name': 'medium', 'size': 2, 'team': 'light'},
        'B': {'name': 'medium', 'size': 2, 'team': 'dark'},
        'c': {'name': 'large', 'size': 3, 'team': 'light'},
        'C': {'name': 'large', 'size': 3, 'team': 'dark'},
        'd': {'name': 'square', 'size': 2, 'team': 'light'},
        'D': {'name': 'square', 'size': 2, 'team': 'dark'}
    }
    
    @staticmethod
    def get_piece_info(piece_char):
        """Get information about a piece"""
        return Piece.PIECE_TYPES.get(piece_char, None)
    
    @staticmethod
    def is_valid_piece(piece_char):
        """Check if character represents a valid piece"""
        return piece_char in Piece.PIECE_TYPES
    
    @staticmethod
    def get_team(piece_char):
        """Get the team of a piece"""
        info = Piece.get_piece_info(piece_char)
        return info['team'] if info else None
    
    @staticmethod
    def get_size(piece_char):
        """Get the size of a piece"""
        info = Piece.get_piece_info(piece_char)
        return info['size'] if info else 1


class BoardValidator:
    """Validates board positions and piece placement"""
    
    @staticmethod
    def check_sink_range(row_max, col_max, row, col):
        """Check if a sink is in the correct position"""
        if (col >= 0 and col < col_max) and (row >= 0 and row < row_max):
            if (row < 3 or row >= row_max - 3) or (col < 3 or col >= col_max - 3):
                return True
        return False
    
    @staticmethod
    def check_piece_range(row_max, col_max, row, col):
        """Check if a piece is in the correct position"""
        if (row >= 0 and row < row_max) and (col >= 0 and col < col_max):
            if (row >= 3 and row < row_max - 3) and (col >= 3 and col < col_max - 3):
                return True
        return False
    
    @staticmethod
    def field_on_board(row, col, board):
        """Check if field is on the board"""
        return 0 <= row < len(board) and 0 <= col < len(board[0])


class MoveValidator:
    """Validates moves according to game rules"""
    
    def __init__(self, board):
        self.board = board
        self.height = len(board)
        self.width = len(board[0])
    
    def is_valid_move(self, row, col, direction):
        """Check if a move is valid"""
        if not self.is_valid_position(row, col):
            return False, "Position out of bounds"
        
        piece = self.board[row][col]
        if not Piece.is_valid_piece(piece):
            return False, "No valid piece at position"
        
        if direction not in ['l', 'r', 'u', 'd']:
            return False, "Invalid direction"
        
        return self.validate_direction_move(row, col, piece, direction)
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < self.height and 0 <= col < self.width
    
    def validate_direction_move(self, row, col, piece, direction):
        """Validate move in specific direction"""
        if direction == 'r':
            return self.validate_rightward_move(row, col, piece)
        elif direction == 'l':
            return self.validate_leftward_move(row, col, piece)
        elif direction == 'u':
            return self.validate_upward_move(row, col, piece)
        elif direction == 'd':
            return self.validate_downward_move(row, col, piece)
        return False, "Invalid direction"
    
    def check_piece_upright(self, row, col, piece):
        """Check if a piece is upright or lying on its side"""
        if piece in ['a', 'A']:
            return True
        
        # Check if piece has extensions
        identifier = str(row * self.width + col)
        has_right_extension = (col + 1 < self.width and self.board[row][col + 1] == identifier)
        has_down_extension = (row + 1 < self.height and self.board[row + 1][col] == identifier)
        
        return not (has_right_extension or has_down_extension)
    
    def validate_rightward_move(self, row, col, piece):
        """Validate rightward movement"""
        is_upright = self.check_piece_upright(row, col, piece)
        
        if piece in ['a', 'A']:
            if col + 1 < self.width and self.board[row][col + 1] == ' ':
                return True, "Valid move"
        elif piece in ['b', 'B']:
            if is_upright:
                if col + 1 < self.width and self.board[row][col + 1] == ' ':
                    return True, "Valid move"
            else:
                if col + 2 < self.width and self.board[row][col + 1] == ' ' and self.board[row][col + 2] == ' ':
                    return True, "Valid move"
        elif piece in ['c', 'C']:
            if is_upright:
                if col + 1 < self.width and self.board[row][col + 1] == ' ':
                    return True, "Valid move"
            else:
                if col + 3 < self.width and all(self.board[row][col + i] == ' ' for i in range(1, 4)):
                    return True, "Valid move"
        elif piece in ['d', 'D']:
            if col + 2 < self.width and self.board[row][col + 1] == ' ' and self.board[row][col + 2] == ' ':
                return True, "Valid move"
        
        return False, "Path blocked or out of bounds"
    
    def validate_leftward_move(self, row, col, piece):
        """Validate leftward movement"""
        is_upright = self.check_piece_upright(row, col, piece)
        
        if piece in ['a', 'A']:
            if col - 1 >= 0 and self.board[row][col - 1] == ' ':
                return True, "Valid move"
        elif piece in ['b', 'B']:
            if is_upright:
                if col - 1 >= 0 and self.board[row][col - 1] == ' ':
                    return True, "Valid move"
            else:
                if col - 2 >= 0 and self.board[row][col - 1] == ' ' and self.board[row][col - 2] == ' ':
                    return True, "Valid move"
        elif piece in ['c', 'C']:
            if is_upright:
                if col - 1 >= 0 and self.board[row][col - 1] == ' ':
                    return True, "Valid move"
            else:
                if col - 3 >= 0 and all(self.board[row][col - i] == ' ' for i in range(1, 4)):
                    return True, "Valid move"
        elif piece in ['d', 'D']:
            if col - 2 >= 0 and self.board[row][col - 1] == ' ' and self.board[row][col - 2] == ' ':
                return True, "Valid move"
        
        return False, "Path blocked or out of bounds"
    
    def validate_upward_move(self, row, col, piece):
        """Validate upward movement"""
        is_upright = self.check_piece_upright(row, col, piece)
        
        if piece in ['a', 'A']:
            if row - 1 >= 0 and self.board[row - 1][col] == ' ':
                return True, "Valid move"
        elif piece in ['b', 'B']:
            if is_upright:
                if row - 1 >= 0 and self.board[row - 1][col] == ' ':
                    return True, "Valid move"
            else:
                if row - 1 >= 0 and self.board[row - 1][col] == ' ':
                    return True, "Valid move"
        elif piece in ['c', 'C']:
            if is_upright:
                if row - 1 >= 0 and self.board[row - 1][col] == ' ':
                    return True, "Valid move"
            else:
                if row - 1 >= 0 and self.board[row - 1][col] == ' ':
                    return True, "Valid move"
        elif piece in ['d', 'D']:
            if row - 1 >= 0 and self.board[row - 1][col] == ' ':
                return True, "Valid move"
        
        return False, "Path blocked or out of bounds"
    
    def validate_downward_move(self, row, col, piece):
        """Validate downward movement"""
        is_upright = self.check_piece_upright(row, col, piece)
        
        if piece in ['a', 'A']:
            if row + 1 < self.height and self.board[row + 1][col] == ' ':
                return True, "Valid move"
        elif piece in ['b', 'B']:
            if is_upright:
                if row + 2 < self.height and self.board[row + 1][col] == ' ' and self.board[row + 2][col] == ' ':
                    return True, "Valid move"
            else:
                if row + 1 < self.height and self.board[row + 1][col] == ' ':
                    return True, "Valid move"
        elif piece in ['c', 'C']:
            if is_upright:
                if row + 3 < self.height and all(self.board[row + i][col] == ' ' for i in range(1, 4)):
                    return True, "Valid move"
            else:
                if row + 1 < self.height and self.board[row + 1][col] == ' ':
                    return True, "Valid move"
        elif piece in ['d', 'D']:
            if row + 2 < self.height and self.board[row + 1][col] == ' ' and self.board[row + 2][col] == ' ':
                return True, "Valid move"
        
        return False, "Path blocked or out of bounds"


class MoveExecutor:
    """Executes moves on the board"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.board = game_state.board
        self.height = game_state.height
        self.width = game_state.width
    
    def execute_move(self, row, col, direction):
        """Execute a move and update game state"""
        if direction in ['l', 'r']:
            self.move_horizontal(row, col, direction)
        elif direction in ['u', 'd']:
            self.move_vertical(row, col, direction)
        
        self.apply_gravity()
        self.check_sinks()
    
    def move_horizontal(self, row, col, direction):
        """Move piece horizontally"""
        piece = self.board[row][col]
        delta = 1 if direction == 'r' else -1
        
        if piece in ['a', 'A']:
            self.board[row][col] = ' '
            self.board[row][col + delta] = piece
        elif piece in ['b', 'B']:
            self.move_medium_piece_horizontal(row, col, delta)
        elif piece in ['c', 'C']:
            self.move_large_piece_horizontal(row, col, delta)
        elif piece in ['d', 'D']:
            self.move_square_piece_horizontal(row, col, delta)
    
    def move_vertical(self, row, col, direction):
        """Move piece vertically"""
        piece = self.board[row][col]
        delta = 1 if direction == 'd' else -1
        
        if piece in ['a', 'A']:
            self.board[row][col] = ' '
            self.board[row + delta][col] = piece
        elif piece in ['b', 'B']:
            self.move_medium_piece_vertical(row, col, delta)
        elif piece in ['c', 'C']:
            self.move_large_piece_vertical(row, col, delta)
        elif piece in ['d', 'D']:
            self.move_square_piece_vertical(row, col, delta)
    
    def move_medium_piece_horizontal(self, row, col, delta):
        """Move medium piece horizontally"""
        piece = self.board[row][col]
        validator = MoveValidator(self.board)
        is_upright = validator.check_piece_upright(row, col, piece)
        
        # Clear current position
        identifier = str(row * self.width + col)
        self.board[row][col] = ' '
        
        # Clear extensions
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == identifier:
                    self.board[i][j] = ' '
        
        # Place in new position
        new_col = col + delta
        self.board[row][new_col] = piece
        
        # Add extensions based on orientation
        new_identifier = str(row * self.width + new_col)
        if is_upright:
            self.board[row + 1][new_col] = new_identifier
        else:
            self.board[row][new_col + 1] = new_identifier
    
    def move_medium_piece_vertical(self, row, col, delta):
        """Move medium piece vertically"""
        piece = self.board[row][col]
        validator = MoveValidator(self.board)
        is_upright = validator.check_piece_upright(row, col, piece)
        
        # Clear current position
        identifier = str(row * self.width + col)
        self.board[row][col] = ' '
        
        # Clear extensions
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == identifier:
                    self.board[i][j] = ' '
        
        # Place in new position
        new_row = row + delta
        self.board[new_row][col] = piece
        
        # Add extensions based on orientation
        new_identifier = str(new_row * self.width + col)
        if is_upright:
            self.board[new_row + 1][col] = new_identifier
        else:
            self.board[new_row][col + 1] = new_identifier
    
    def move_large_piece_horizontal(self, row, col, delta):
        """Move large piece horizontally"""
        piece = self.board[row][col]
        validator = MoveValidator(self.board)
        is_upright = validator.check_piece_upright(row, col, piece)
        
        # Clear current position
        identifier = str(row * self.width + col)
        self.board[row][col] = ' '
        
        # Clear extensions
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == identifier:
                    self.board[i][j] = ' '
        
        # Place in new position
        new_col = col + delta
        self.board[row][new_col] = piece
        
        # Add extensions based on orientation
        new_identifier = str(row * self.width + new_col)
        if is_upright:
            self.board[row + 1][new_col] = new_identifier
            self.board[row + 2][new_col] = new_identifier
        else:
            self.board[row][new_col + 1] = new_identifier
            self.board[row][new_col + 2] = new_identifier
    
    def move_large_piece_vertical(self, row, col, delta):
        """Move large piece vertically"""
        piece = self.board[row][col]
        validator = MoveValidator(self.board)
        is_upright = validator.check_piece_upright(row, col, piece)
        
        # Clear current position
        identifier = str(row * self.width + col)
        self.board[row][col] = ' '
        
        # Clear extensions
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == identifier:
                    self.board[i][j] = ' '
        
        # Place in new position
        new_row = row + delta
        self.board[new_row][col] = piece
        
        # Add extensions based on orientation
        new_identifier = str(new_row * self.width + col)
        if is_upright:
            self.board[new_row + 1][col] = new_identifier
            self.board[new_row + 2][col] = new_identifier
        else:
            self.board[new_row][col + 1] = new_identifier
            self.board[new_row][col + 2] = new_identifier
    
    def move_square_piece_horizontal(self, row, col, delta):
        """Move square piece horizontally"""
        piece = self.board[row][col]
        
        # Clear current position
        identifier = str(row * self.width + col)
        self.board[row][col] = ' '
        
        # Clear extensions
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == identifier:
                    self.board[i][j] = ' '
        
        # Place in new position
        new_col = col + delta
        self.board[row][new_col] = piece
        
        # Add 2x2 extensions
        new_identifier = str(row * self.width + new_col)
        self.board[row + 1][new_col] = new_identifier
        self.board[row][new_col + 1] = new_identifier
        self.board[row + 1][new_col + 1] = new_identifier
    
    def move_square_piece_vertical(self, row, col, delta):
        """Move square piece vertically"""
        piece = self.board[row][col]
        
        # Clear current position
        identifier = str(row * self.width + col)
        self.board[row][col] = ' '
        
        # Clear extensions
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == identifier:
                    self.board[i][j] = ' '
        
        # Place in new position
        new_row = row + delta
        self.board[new_row][col] = piece
        
        # Add 2x2 extensions
        new_identifier = str(new_row * self.width + col)
        self.board[new_row + 1][col] = new_identifier
        self.board[new_row][col + 1] = new_identifier
        self.board[new_row + 1][col + 1] = new_identifier
    
    def apply_gravity(self):
        """Apply gravity to all pieces"""
        for col in range(self.width):
            for row in range(self.height - 2, -1, -1):
                if self.board[row][col] != ' ' and self.board[row][col] != 's' and self.board[row][col] != 'x':
                    piece = self.board[row][col]
                    if Piece.is_valid_piece(piece):
                        target_row = row
                        
                        while (target_row + 1 < self.height and 
                               self.board[target_row + 1][col] == ' '):
                            target_row += 1
                        
                        if target_row != row:
                            self.board[row][col] = ' '
                            self.board[target_row][col] = piece
    
    def check_sinks(self):
        """Check for pieces that have fallen into sinks"""
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 's':
                    if (row > 0 and 
                        Piece.is_valid_piece(self.board[row - 1][col])):
                        piece = self.board[row - 1][col]
                        team = Piece.get_team(piece)
                        
                        if team == 'light':
                            self.game_state.light_sinked_pieces += 1
                        else:
                            self.game_state.dark_sinked_pieces += 1
                        
                        self.board[row - 1][col] = ' '


class BoardReader:
    """Reads board configuration from input"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.board = game_state.board
        self.height = game_state.height
        self.width = game_state.width
    
    def read_board(self):
        """Read board configuration from stdin"""
        while True:
            try:
                line = stdio.readLine()
                if line == '#':
                    break
            except EOFError:
                break
            
            board_input = line.split()
            type_of_object = board_input[0]
            
            if type_of_object == 'x':
                row = int(board_input[1])
                col = int(board_input[2])
                
                if BoardValidator.field_on_board(row, col, self.board):
                    self.board[row][col] = 'x'
            
            elif type_of_object == 's':
                piece_size = int(board_input[1])
                row = int(board_input[2])
                col = int(board_input[3])
                
                if not BoardValidator.field_on_board(row, col, self.board):
                    continue
                    
                if not BoardValidator.check_sink_range(self.height, self.width, row, col):
                    stdio.writeln("ERROR: Sink in the wrong position")
                    sys.exit(1)
                    
                for i in range(row, min(row + piece_size, self.height)):
                    for j in range(col, min(col + piece_size, self.width)):
                        self.board[i][j] = 's'
            
            elif type_of_object in ['d', 'l']:
                piece_type = board_input[1]
                row = int(board_input[2])
                col = int(board_input[3])
                
                if not BoardValidator.field_on_board(row, col, self.board):
                    continue
                    
                if not BoardValidator.check_piece_range(self.height, self.width, row, col):
                    stdio.writeln("ERROR: Piece in the wrong position")
                    sys.exit(1)
                    
                if type_of_object == 'd':
                    piece_upper_case = piece_type.upper()
                    self.board[row][col] = piece_upper_case
                else:
                    self.board[row][col] = piece_type
        
        self.field_for_bottom_left_most()
        return self.board
    
    def field_for_bottom_left_most(self):
        """Update the fields for multi-cell pieces"""
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] in ['b', 'B', 'c', 'C', 'd', 'D']:
                    identifier = str(i * self.width + j)
                    piece = self.board[i][j]
                    
                    if piece in ['b', 'B']:
                        # Size 2 piece
                        if i + 1 < self.height and self.board[i + 1][j] == ' ':
                            self.board[i + 1][j] = identifier
                        elif j + 1 < self.width and self.board[i][j + 1] == ' ':
                            self.board[i][j + 1] = identifier
                            
                    elif piece in ['c', 'C']:
                        # Size 3 piece
                        if i + 2 < self.height and self.board[i + 1][j] == ' ' and self.board[i + 2][j] == ' ':
                            self.board[i + 1][j] = identifier
                            self.board[i + 2][j] = identifier
                        elif j + 2 < self.width and self.board[i][j + 1] == ' ' and self.board[i][j + 2] == ' ':
                            self.board[i][j + 1] = identifier
                            self.board[i][j + 2] = identifier
                            
                    elif piece in ['d', 'D']:
                        # 2x2 piece
                        if (i + 1 < self.height and j + 1 < self.width and 
                            self.board[i + 1][j] == ' ' and self.board[i][j + 1] == ' ' and 
                            self.board[i + 1][j + 1] == ' '):
                            self.board[i + 1][j] = identifier
                            self.board[i][j + 1] = identifier
                            self.board[i + 1][j + 1] = identifier


class BoardPrinter:
    """Handles board printing for text mode"""
    
    @staticmethod
    def print_board(board):
        """Print the board to stdout"""
        height = len(board)
        width = len(board[0])
        
        # Print column numbers
        stdio.write('    ' + '  '.join(str(i) for i in range(width)))
        stdio.writeln()
        
        # Print horizontal line
        stdio.write('  ' + '+--' * width + '+')
        stdio.writeln()
        
        # Print each row from top to bottom (reverse order)
        for i in range(height - 1, -1, -1):
            row = []
            for j in range(width):
                cell = board[i][j]
                
                if BoardPrinter.is_identifier(board, cell):
                    row.append(cell)
                elif cell == 's':
                    row.append(' s')
                elif cell == 'x':
                    row.append(' x')
                elif cell in ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']:
                    row.append(' ' + cell)
                else:
                    row.append('  ')
            
            stdio.write(str(i) + ' |' + '|'.join(row) + '|')
            stdio.writeln()
            stdio.write('  ' + '+--' * width + '+')
            stdio.writeln()
    
    @staticmethod
    def is_identifier(board, cell):
        """Check if the cell is an identifier"""
        try:
            num = int(cell)
            num_rows = len(board)
            num_columns = len(board[0])
            
            if 0 <= num < num_rows * num_columns:
                return True
        except ValueError:
            pass
        
        return False


class TextGameMode:
    """Handles text-based game mode"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.validator = MoveValidator(game_state.board)
        self.executor = MoveExecutor(game_state)
        self.board_reader = BoardReader(game_state)
        self.is_light_player = True
        self.move_count = 0
    
    def run(self):
        """Run the text-based game"""
        # Read board configuration
        self.board_reader.read_board()
        BoardPrinter.print_board(self.game_state.board)
        
        # Main game loop
        while True:
            try:
                line = stdio.readLine()
            except EOFError:
                BoardPrinter.print_board(self.game_state.board)
                stdio.writeln("Partial game")
                sys.exit(0)
            
            if not line:
                BoardPrinter.print_board(self.game_state.board)
                stdio.writeln("Partial game")
                sys.exit(0)
            
            move = line.split()
            if len(move) != 3:
                stdio.writeln("ERROR: Invalid move format")
                continue
                
            try:
                row = int(move[0])
                col = int(move[1])
                action = move[2]
            except ValueError:
                stdio.writeln("ERROR: Invalid move format")
                continue

            # Validate move
            valid, message = self.validator.is_valid_move(row, col, action)
            if not valid:
                stdio.writeln(f"ERROR: {message}")
                continue

            # Execute move
            self.executor.execute_move(row, col, action)
            self.move_count += 1

            # Print board after move
            BoardPrinter.print_board(self.game_state.board)

            # Check for win condition
            winner = self.game_state.check_win_condition()
            if winner:
                stdio.writeln(f"{winner.capitalize()} wins")
                sys.exit(0)

            # Switch player
            self.game_state.switch_player()
            self.is_light_player = not self.is_light_player
            stdio.writeln(f"Next player: {'light' if self.is_light_player else 'dark'}")
class GUIGameMode:
    """Handles GUI-based game mode"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.validator = MoveValidator(game_state.board)
        self.executor = MoveExecutor(game_state)
        self.board_reader = BoardReader(game_state)
        self.is_light_player = True
        self.root = tk.Tk()
        self.root.title("Board Game")
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()
        self.board_reader.read_board()  # <-- Add this line!
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
    
    def draw_board(self):
        """Draw the board on the canvas"""
        self.canvas.delete("all")
        height = len(self.game_state.board)
        width = len(self.game_state.board[0])
        
        cell_size = 600 // max(height, width)
        
        for i in range(height):
            for j in range(width):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                piece = self.game_state.board[i][j]
                
                if piece == 's':
                    color = 'blue'
                elif piece == 'x':
                    color = 'red'
                elif Piece.is_valid_piece(piece):
                    color = 'green' if Piece.get_team(piece) == 'light' else 'black'
                else:
                    color = 'white'
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                if piece != ' ':
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=piece, font=("Arial", 16))
        
        # Draw grid lines
        for i in range(height + 1):
            self.canvas.create_line(0, i * cell_size, width * cell_size, i * cell_size)
        for j in range(width + 1):
            self.canvas.create_line(j * cell_size, 0, j * cell_size, height * cell_size)
    
    def on_click(self, event):
        """Handle click events on the canvas"""
        cell_size = 600 // max(len(self.game_state.board), len(self.game_state.board[0]))
        
        col = event.x // cell_size
        row = event.y // cell_size  # Fix: y increases downward in Tkinter

        if not (0 <= row < len(self.game_state.board) and 0 <= col < len(self.game_state.board[0])):
            messagebox.showerror("Invalid Move", "Click outside the board area")
            return

        piece = self.game_state.board[row][col]
        if not Piece.is_valid_piece(piece):
            messagebox.showerror("Invalid Move", "No valid piece at this position")
            return

        # For demo, always try to move right ('r')
        valid, message = self.validator.is_valid_move(row, col, 'r')
        if not valid:
            messagebox.showerror("Invalid Move", message)
            return

        self.executor.execute_move(row, col, 'r')
        self.draw_board()

        winner = self.game_state.check_win_condition()
        if winner:
            messagebox.showinfo("Game Over", f"{winner.capitalize()} wins!")
            self.root.quit()

        self.game_state.switch_player()
        self.is_light_player = not self.is_light_player
        messagebox.showinfo("Next Player", f"Next player: {'light' if self.is_light_player else 'dark'}")

def print_usage():
    print("Usage: python gameBoardText.py <height> <width> <mode>")
    print("  <height>: Board height (8, 9, or 10)")
    print("  <width>: Board width (8, 9, or 10)")
    print("  <mode>: 0 for text mode, 1 for GUI mode")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print_usage()
        sys.exit(1)

    try:
        height = int(sys.argv[1])
        width = int(sys.argv[2])
        mode = int(sys.argv[3])
    except ValueError:
        print_usage()
        sys.exit(1)

    if height not in [8, 9, 10] or width not in [8, 9, 10]:
        print("ERROR: Height and width must be 8, 9, or 10.")
        sys.exit(1)

    game_state = GameState(height, width)

    if mode == 0:
        # Text mode
        game = TextGameMode(game_state)
        game.run()
    elif mode == 1:
        # GUI mode
        game = GUIGameMode(game_state)
        game.root.mainloop()
    else:
        print("ERROR: Mode must be 0 (text) or 1 (GUI).")
        sys.exit(1)
