"""
Generates an AI move. The AI ratings from 1500 to 1700 are played by the 
a negamax algorithim with alpha-beta pruning, while the rest of the rating ranges
are played by the stockfish engine.
"""
import chess.engine
import position_status
ROW_DIM =  8

# These piece-square tables represent the positional advantages each piece
# has at certain squares depending on their mobility and control options.
# Values from: (https://www.chessprogramming.net/using-excel-to-help-create-piece-square-tables/)
white_pawn_values = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [18, 22,  34,  50,  50,  34, 22, 18],
        [6, 12, 25, 40, 40, 25, 12, 6],
        [-3, 3,	17,	28,	28,	17,	3, -3],
        [-10, -5, 10, 20, 20, 10, -5, -10],
        [-10, -5, 5, 15, 15, 5, -5, -10],
        [-10, -5, 5, 10, 10, 5, -5, -10],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
black_pawn_values = white_pawn_values[::-1]

white_knight_values = [
        [-60, -40, -30, -30,-30, -30, -40, -60],
        [-40, 20, 40, 40, 40, 40, 20, -40],
        [-40, 45, 60, 70, 70, 60, 45, -40],
        [-40, 40, 50, 50, 50, 50, 40, -40],
        [-40, 10, 40, 35, 35, 40, 10, -40],
        [-40, 0, 30, 20, 20, 30, 0, -40],
        [-55, -40, -10, 10, 10, -10, -40, -55],
        [-70, -20, -25, -15, -15, -25, -20, -70]
    ]
black_knight_values = white_knight_values[::-1]

white_bishop_values = [
        [-10, -8, -6, -4, -4, -6, -8, -10],
        [0, 20,  10,  10,  10,  10, 20, 0],
        [10,  20,  30,  35,  35,  30,  20, 10],
        [10,  30,  30,  35,  35,  30,  30, 10],
        [10,  10,  25,  30,  30,  25,  10, 10],
        [-15,  15,  25,  20,  20,  25,  15, -15],
        [-18, 20,  15,  10,  10,  15, 20, -18],
        [-20, -15, -10, -10, -10, -10, -15, -20]
    ]
black_bishop_values = white_bishop_values[::-1]

white_rook_values = [
        [-10, -8, 0, 5, 5, 0, -8, -10],
        [0, 0, 5, 10, 10, 5, 0, 0],
        [-10, -8, 4, 8, 8, 4, -8, -10],
        [-10, -8, 4, 6, 6, 4, -8, -10],
        [-10, -8, 4, 5, 5, 4, -8, -10],
        [-10, -8, 4, 5, 5, 4, -8, -10],
        [-10, -8, 0, 5, 5, 0, -8, -10],
        [-10, -8, 0, 5, 5, 0, -8, -10],
    ]
black_rook_values = white_rook_values[::-1]

white_queen_values = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-10, -10, -5, 0, 0, -5, -10, -10],
        [-20, -15,  -5,  0,  0,  -5, -15, -20],
        [-30, -20, -10, 0, 0, -10, -20, -30]
    ]
black_queen_values = white_queen_values[::-1]

white_king_values = [
        [-55, -55, -60, -70, -70, -60, -55, -55],
        [-55, -55, -60, -70, -70, -60, -55, -55],
        [-55, -55, -60, -70, -70, -60, -55, -55],
        [-55, -55, -60, -70, -70, -60, -55, -55],
        [-50, -50, -55, -60, -60, -55, -50, -50],
        [-40,  -40,  -45,  -50,  -50,  -45,  -40, -40],
        [-30, -30,  -30,  -35,  -35,  -30, -30, -30],
        [-3, 0, 0, -10, -10, -8, 0, -3]
    ]
black_king_values = white_king_values[::-1]

# Plays the best ai move depending on what difficulty/rating was set. The more advanced rating
# levels use the stockfish engine.
def ai_move(difficulty, turn, fen_board):
    engine = chess.engine.SimpleEngine.popen_uci("./Stockfish/stockfish")
    copied_fen_board = fen_board.copy()
    if (fen_board.is_checkmate()):
        return fen_board
    if difficulty == 1500:
        negamax(2, copied_fen_board, turn, copied_fen_board.legal_moves, 2, -9999, 9999)
        if best_move in fen_board.legal_moves:
            fen_board.push(best_move)
        else: 
            legal_moves = list(fen_board.legal_moves)
            fen_board.push(legal_moves[0])
    elif difficulty == 1600:
        negamax(3, copied_fen_board, turn, copied_fen_board.legal_moves, 3, -9999, 9999)
        if best_move in fen_board.legal_moves:
            fen_board.push(best_move)
        else: 
            legal_moves = list(fen_board.legal_moves)
            fen_board.push(legal_moves[0])
    elif difficulty == 1700:
        negamax(4, copied_fen_board, turn, copied_fen_board.legal_moves, 4, -9999, 9999)
        if best_move in fen_board.legal_moves:
            fen_board.push(best_move)
        else: 
            legal_moves = list(fen_board.legal_moves)
            fen_board.push(legal_moves[0])
    elif difficulty == 1800:
        limit = chess.engine.Limit(depth=1)
        result = engine.play(fen_board, limit)  
        fen_board.push(result.move)
    elif difficulty == 1900:
        limit = chess.engine.Limit(depth=2)
        result = engine.play(fen_board, limit)  
        fen_board.push(result.move)
    elif difficulty == 2000:
        limit = chess.engine.Limit(depth=3)
        result = engine.play(fen_board, limit)  
        fen_board.push(result.move)
    elif difficulty == 2100:
        limit = chess.engine.Limit(depth=3)
        result = engine.play(fen_board, limit)  
        fen_board.push(result.move)
    elif difficulty == 2200:
        limit = chess.engine.Limit(depth=4)
        result = engine.play(fen_board, limit)  
        fen_board.push(result.move)
    engine.quit()
    return fen_board


# Apply negamax algorithim recursively with alpha beta pruning to 
# evaluate root positions for a certain depth
def negamax(curr_depth, fen_board, turn, moves, max_depth, alpha, beta):
    global best_move
    board = position_status.fen_to_board(fen_board.fen())
    if curr_depth == 0:
        if turn == 'w':
            return evaluate_board_score(fen_board, board, turn)
        else: 
            return -1 * evaluate_board_score(fen_board, board, turn)
    max = -9999
    if not fen_board.is_checkmate():
        for move in moves:
            fen_board.push(move)
            if turn == 'b':
                turn = 'w'
            else: 
                turn = 'b'
            next_moves = fen_board.legal_moves
            position_score = -negamax(curr_depth - 1, fen_board, turn, next_moves, max_depth, -beta, -alpha)
            if position_score > max:
                max = position_score
                if curr_depth == max_depth:
                    best_move = move
            fen_board.pop()
            if max > alpha:
                alpha = max
            if alpha >= beta:
                break
    return max


# Determines piece value based on its raw value (e.g. white pawn is always
# worth 100 points) along with which square it is on the board (positional 
# value). White values are positive, and black values are negative. This 
# function returns their sum.
def evaluate_board_score(fen_board, board, turn):
    white_value = 0
    black_value = 0
    for row in range(ROW_DIM):
        for column in range(ROW_DIM):
            piece = board[row][column]
            if fen_board.is_checkmate():
                if turn == 'w':
                    return 9999
                else: 
                    return -9999
            if piece == 'e':
                pass
            else:
                if (piece[0] == 'w'):
                    if (piece[1] == 'p'):
                        white_value += 100 + white_pawn_values[row][column]
                    elif (piece[1] == 'b'):
                        white_value += 300 + white_bishop_values[row][column]
                    elif (piece[1] == 'n'):
                        white_value += 300 + white_knight_values[row][column]
                    elif (piece[1] == 'r'):
                        white_value += 500 + white_rook_values[row][column]
                    elif (piece[1] == 'q'): 
                        white_value += 900 + white_queen_values[row][column]
                    elif (piece[1] == 'k'):
                        white_value += 9000 + white_king_values[row][column]
                elif (piece[0] == 'b'):
                    if (piece[1] == 'p'):
                        black_value += 100+ black_pawn_values[row][column]
                    elif (piece[1] == 'b'):
                        black_value += 300 + black_bishop_values[row][column]
                    elif (piece[1] == 'n'):
                        black_value += 300 + black_knight_values[row][column]
                    elif (piece[1] == 'r'):
                        black_value += 500 + black_rook_values[row][column]
                    elif (piece[1] == 'q'): 
                        black_value += 900 + black_queen_values[row][column]
                    elif (piece[1] == 'k'):
                        black_value += 9000 + black_king_values[row][column]             
    return white_value - black_value


    