import chess
""" 
Base alpha-beta search algorithm
Feel free to modify the depth parameter.
"""
def alpha_beta_search(board: chess.Board, evaluate_board) -> chess.Move:
    """
    Alpha-beta pruning algorithm, given a evaulate board. 
    """
    depth: int = 4
    best_move = None
    best_value = -float('inf') if board.turn == chess.WHITE else float('inf')

    def alpha_beta(board, depth, alpha, beta, maximizing):
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)
        
        if maximizing: # If we are maximizing, then it is whites turn, i.e., we are looking for best possible move as white
            max_eval = -float('inf')
            # Loop through all possible moves as white
            for move in board.legal_moves:
                # Make move
                board.push(move)
                # Recursively call alpha_beta
                move_eval = alpha_beta(board, depth - 1, alpha, beta, False)
                # Undo the move
                board.pop()
                max_eval = max(max_eval, move_eval)
                alpha = max(alpha, move_eval) # update alpha value
                if beta <= alpha: # Prune the tree
                    break
            return max_eval
        else: # If we are minimizing, then it is blacks turn, i.e., we are looking for best possible move as black
            min_eval = float('inf')
            # Loop through all possible moves as black
            for move in board.legal_moves:
                board.push(move)
                move_eval = alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop() # undo the move
                min_eval = min(min_eval, move_eval)
                beta = min(beta, move_eval)
                if beta <= alpha:
                    break
            return min_eval

    for move in board.legal_moves:
        # make a move
        board.push(move) 
        # Check the value of the made move
        move_value = alpha_beta(board, depth - 1, -float('inf'), float('inf'), not board.turn)
        # undo the move
        board.pop() 
        
        # Keep track of the best move
        if board.turn == chess.WHITE:
            if move_value > best_value:
                best_value = move_value
                best_move = move
        else:
            if move_value < best_value:
                best_value = move_value
                best_move = move
    return best_move
