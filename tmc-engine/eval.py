import chess

PAWN_RANK_BONUS = 0.05
CHECK_PENALTY = -1

""" 
Base Example evaluation function. 
You could, for example, change the values of the pieces (piece_values dictionary) with different values 
found in the linked wikipedia article. 
"""
def simple_board_eval(board: chess.Board) -> int:
    """
    Basic board evaluation function, which adds up the value of all the pieces on the board.
    Returns a positive value if White is winning and a negative value if Black is winning.
    Piece values from: https://en.wikipedia.org/wiki/Chess_piece_relative_value)
    """
    # If the game is over, return a very large value for checkmate or 0 for a draw
    if board.is_checkmate():
        # If it's Black's turn and Black is checkmated, White wins
        if board.turn == chess.BLACK:
            return 10000
        # If it's White's turn and White is checkmated, Black wins
        else:
            return -10000
    elif board.is_stalemate() or board.is_insufficient_material():
        # If is its a draw, then nobody wins and is equal 
        return 0

    # Assign values to pieces
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    # Calculate the total value of pieces for both White and Black
    value = 0
    for piece_type in piece_values:
        # Count the number of each type of piece for White and Black, and add or subtract accordingly
        white_count = len(board.pieces(piece_type, chess.WHITE))
        black_count = len(board.pieces(piece_type, chess.BLACK))
        value += white_count * piece_values[piece_type]
        value -= black_count * piece_values[piece_type]

    return value

def evaluate_board(board: chess.Board) -> float:
    """
    Basic board evaluation function, which adds up the value of all the pieces on the board.
    Returns a positive value if White is winning and a negative value if Black is winning.
    Piece values from: https://en.wikipedia.org/wiki/Chess_piece_relative_value)

    TODO: 
        Bonus for having more control (squares covered by piece)
        Bonus for having a protected piece
        Bonus for having pieces around the king
        Bonus for restricting enemy king movement
        Penalty for attacking a piece with more defenders than attackers
    """
    # If the game is over, return a very large value for checkmate or 0 for a draw
    if board.is_checkmate():
        # If it's Black's turn and Black is checkmated, White wins
        if board.turn == chess.BLACK:
            return 10000
        # If it's White's turn and White is checkmated, Black wins
        else:
            return -10000
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        # If is its a draw, then nobody wins and is equal 
        return 0

    # Assign values to pieces
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 4,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    # Calculate the total value of pieces for both White and Black
    value = 0
    for piece_type in piece_values:
        # Count the number of each type of piece for White and Black, and add or subtract accordingly
        white_all_pieces_of_type = board.pieces(piece_type, chess.WHITE)        
        black_all_pieces_of_type = board.pieces(piece_type, chess.BLACK)        

        for piece in white_all_pieces_of_type:
            if piece.piece_type == chess.PAWN:
                value += 1 * PAWN_RANK_BONUS * chess.square_rank(piece) 

        for piece in black_all_pieces_of_type:
            if piece.piece_type == chess.PAWN:
                value += -1 * PAWN_RANK_BONUS * chess.square_rank(piece) 

        white_count = len(white_all_pieces_of_type)
        black_count = len(black_all_pieces_of_type)
        value += white_count * piece_values[piece_type]
        value -= black_count * piece_values[piece_type]

    # -1 for black if white is in check and the other way around
    value += -CHECK_PENALTY if board.turn else CHECK_PENALTY * board.is_check()

    return value


if __name__ == "__main__":
    board = chess.Board("r1bqk2r/2pp1ppp/p1n2n2/1p2p3/1b2P3/1B1P1N2/PPP2PPP/RNBQ1RK1 b kq - 0 7")
    print(board)
    print(evaluate_board(board))
