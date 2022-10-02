"""
Holds information about the current board state, including which color's turn
it is, and the board represented by the current fen.
"""
import chess

# Holds a 2d board array representing the position, and the turn
class PositionStatus:
    def __init__(self, fen):
        self.board = fen_to_board(fen)
        if "w" in fen:
            self.turn = "w"
        else: 
            self.turn = "b"


# Parses fen to a board that is a 2d array where 'e' denotes an empty square,
#  and b_ or w_ denotes a piece. The underscore can be any of the letters that
#  represent the different pieces.
def fen_to_board(fen):
    board = []
    for row in fen.split('/'):
        curr_row = []
        for char in row:
            if char == ' ':
                break
            elif char in '12345678':
                curr_row.extend(['e'] * int(char))
            elif char > 'Z':
                curr_row.append('b' + char)
            else:
                curr_row.append('w' + char.lower())
        board.append(curr_row)
    return board

