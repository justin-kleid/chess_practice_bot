"""
Responsible for all of the game logic, piece movement, and game GUI. Chess 
positions are represented with FEN: a notation describing where all the pieces 
are. The init_game function also handles all the settings chosen in the menu.
# Each '/' in the FEN seperates the next row starting from the 8th rank
"""
import chess
import chess.engine
import chess.polyglot
import pygame as p
import position_status, chess_ai


ROW_DIM =  8
SQUARE_DIM = 50
BLUE = (8, 96, 168)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PIECES = {}
# IMAGE_TAGS: first letter represents piece color, second letter represents piece initial letter (with n for knight)
IMAGE_TAGS = ['bb', 'bk', 'bn', 'bq', 'br', 'bp', 'wb', 'wk', 'wn', 'wp', 'wq', 'wr']


# Load chess piece pngs into the PIECES dictionary where each tag ('bb', etc) corresponds to a piece png
def load_chess_pngs(): 
    for tag in IMAGE_TAGS:
        PIECES[tag] = p.transform.scale(p.image.load("images/" + tag + ".png"), (SQUARE_DIM, SQUARE_DIM))


# Initialize chess game
def init_game(display, clock, single_player_mode, difficulty, start_color):
    p.display.set_caption("My Board")
    load_chess_pngs()
    fen_board = chess.Board() # Initialize the starting board and tracks fen
    fen = fen_board.fen()
    piece_selection = False
    run = True
    drag = False
    while run:
        ps = position_status.PositionStatus(fen)
        board = ps.board
        x, y, piece = square_under_mouse(fen, board)
        your_turn = human_turn(ps.turn, single_player_mode, start_color)
        if your_turn: # Human decided move
            for event in p.event.get(): # Process user interaction with the gui
                if event.type == p.QUIT:
                    run = False
                if event.type == p.KEYDOWN:
                    if event.key == p.K_u and fen_board.move_stack: # undo move
                        if single_player_mode:
                            fen_board.pop()
                            fen_board.pop()
                        else: 
                            fen_board.pop()
                        fen = refresh_board(display, fen_board)
                    if event.key == p.K_r and fen_board.move_stack: # reset game
                        fen_board.reset()
                        fen = refresh_board(display, fen_board)
                if event.type == p.MOUSEBUTTONDOWN: # Checks the piece clicked
                    drag = True
                    if piece != 'e': 
                        piece_selection = True
                        start_coord = chess_notation_converter(x, y, piece)
                    chosen_piece = piece
                    start_x, start_y = x, y
                if event.type == p.MOUSEBUTTONUP: # Checks validity of drop square for piece
                    if piece_selection: 
                        end_x, end_y, _ = square_under_mouse(fen, board)
                        end_coord = chess_notation_converter(end_x, end_y, chosen_piece)
                        if start_coord != end_coord:
                            move = chess.Move.from_uci(start_coord + end_coord) 
                            if (fen_board.is_legal(move)):
                                fen_board.push(move)
                                fen = refresh_board(display, fen_board)
                        piece_selection = False 
                        drag = False 
        else: # AI determined move
            with chess.polyglot.open_reader("openings/baron30.bin") as reader:
                entry = reader.get(fen_board)
                if entry == None: # Triggers if no more opening theory is left
                    fen_board = chess_ai.ai_move(difficulty, ps.turn, fen_board)
                    fen = refresh_board(display, fen_board)
                else: # Opening move
                    move = chess.Move.from_uci(str(entry.move)) 
                    fen_board.push(move)
                    fen = refresh_board(display, fen_board)
        create_board(display)
        fen_to_pieces(fen, display)
        if drag:
            animate_piece_drag(display, fen, ps, chosen_piece, start_x, start_y) 
        else: 
            select_square(display, x, y)
        if (fen_board.is_stalemate() or fen_board.can_claim_draw()):
            return "draw"
        if (fen_board.is_checkmate()):
            return "mate"
        p.display.flip()
        clock.tick(60)
        p.display.update()
    return "exit"


# Returns true if it is a human's to move, and false if it is the computer's 
def human_turn(turn, single_player_mode, start_color):
    if single_player_mode:
        return (turn == 'w' and start_color == 'white') or (turn == 'b' and start_color == 'black')
    else: 
        return True

# Generates the board display (white and blue checkered squares)
def create_board(display):
    count = 0
    display.fill(WHITE)
    # Color in every other square as blue into the white background
    for row in range(ROW_DIM):
        for column in range(ROW_DIM):
            if count % 2 == 0:
                p.draw.rect(display, BLUE, (row * SQUARE_DIM, column * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM))
            count += 1
        count -= 1
    p.draw.rect(display, BLACK, (0, 0, SQUARE_DIM * ROW_DIM, SQUARE_DIM * ROW_DIM), 2)


# Uses the position's fen to draw the pieces in the correct locations.
def fen_to_pieces(fen, display):
    curr_row = 0
    for row in fen.split('/'):
        column = 0
        for char in row:
            if char == ' ':
                break
            elif char in '12345678':
                column += int(char)
            elif char > 'Z':
                tag = 'b' + char
                display.blit(PIECES[tag], p.Rect(column * SQUARE_DIM, curr_row * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM))
                column += 1
            else:
                tag = 'w' + char.lower()
                display.blit(PIECES[tag], p.Rect(column * SQUARE_DIM, curr_row * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM))
                column += 1
        curr_row += 1

# Given some change to the board and its fen, refresh the gui of the board
def refresh_board(display, fen_board):
    fen = fen_board.fen()
    fen_to_pieces(fen, display) #!!! RETURN FEN
    return fen 

# Returns the column (x) and row (y) of the mouse location, and the piece 
# if one is there. 
def square_under_mouse(fen, board):
    cursor_position = p.mouse.get_pos()
    x = cursor_position[0] // SQUARE_DIM
    y = cursor_position[1] // SQUARE_DIM
    piece = board[y][x]
    return x, y, piece

# Given the numerical x, y coordinates (ranging from 0-7), return the chess 
# notation coordinates (e.g. (7, 7) --> (h1)). For a promotion, an extra q
# is tagged to the coordinate for queen promotion.
def chess_notation_converter(x, y, piece):
    columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    rows = ['8', '7', '6', '5', '4', '3', '2', '1']
    column_letter = columns[x]
    row_number = rows[y]
    if ((piece[0] == 'w' and piece[1] == 'p' and int(row_number) == 8) or 
        (piece[0] == 'b' and piece[1] == 'p' and int(row_number) == 1)):
        return column_letter + row_number + 'q'
    return column_letter + row_number

# Highlight the square that the mouse hovers over in red 
def select_square(display, x, y):
    p.draw.rect(display, RED, (x * SQUARE_DIM, y * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM), 2)

# Handles the piece dragging animation.
def animate_piece_drag(display, fen, ps, chosen_piece, start_x, start_y):
    x, y, _ = square_under_mouse(fen, ps.board)
    if (chosen_piece[0] == ps.turn):
        p.draw.rect(display, (194, 197, 204), (start_x * SQUARE_DIM, start_y * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM))
        display.blit(PIECES[chosen_piece], (p.Rect(x * SQUARE_DIM, y * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM)))
        display.blit(PIECES[chosen_piece], (p.Rect(x * SQUARE_DIM, y * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM)))
        p.draw.rect(display, GREEN, (x * SQUARE_DIM, y * SQUARE_DIM, SQUARE_DIM, SQUARE_DIM), 2)



