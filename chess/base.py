# ---------------------------------------------------------------------------------------
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# --------------------------------------------------------------------------------------


# To run: python3 base.py, make sure you have chess installed (pip install chess)
import chess 

""" 
Base Engine Class
DO NOT MODIFY
"""
# Base classes
class ExampleEngine:
    student_name: str = ''
    student_number: int = 0
    notes: str = ''
    def __init__(self, evaluate_board, search_algorithm):
        self.evaluate_board = evaluate_board
        self.search_algorithm = search_algorithm

    def make_move(self, board: chess.Board) -> chess.Move:
        return self.search_algorithm(board, self.evaluate_board)
    
    def __str__(self):
        return f"{self.student_name}_{self.student_number}"


""" 
Base engine class factory function
DO NOT MODIFY
"""
# Class factory function 
def create_engine_class(evaluate_board, search_algorithm, student_name, student_number, notes=''):
    class CustomEngine(ExampleEngine):
        def __init__(self):
            super().__init__(evaluate_board, search_algorithm)
    CustomEngine.student_name = student_name
    CustomEngine.student_number = student_number
    CustomEngine.notes = notes
    return CustomEngine


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


""" 
To test your evaluation or search function, you can use the play_game function against a search algorithm that picks a random move at each turn. 
DO NOT MODIFY
"""

import time
import chess.pgn
def play_game(engine1: ExampleEngine, engine2: ExampleEngine) -> tuple[chess.pgn.Game, str, dict[str, float]]:
    """ 
    Engine 1: White, Engine 2: Black
    returns the pgn of the game and the result string(1-0 for white win, 0-1 for black win, 1/2-1/2 for draw)
    You can copy and paste the pgn (print(pgn)) directly into https://lichess.org/paste to view the game. 
    """
    board = chess.Board()
    move_times_engine1: list[float] = []
    move_times_engine2: list[float] = []
    while not board.is_game_over():
        mveng1 = time.thread_time()
        move = engine1.make_move(board)
        mveng1 = time.thread_time() - mveng1
        board.push(move)
        if board.is_game_over():
            break
        mveng2 = time.thread_time()
        move = engine2.make_move(board)
        mveng2 = time.thread_time() - mveng2
        board.push(move)
        move_times_engine1.append(mveng1)
        move_times_engine2.append(mveng2)
    
    avg_mvtime_eng1 = sum(move_times_engine1) / len(move_times_engine1)
    avg_mvtime_eng2 = sum(move_times_engine2) / len(move_times_engine2)
    pgn = chess.pgn.Game.from_board(board)
    pgn.headers['White'] = str(engine1)
    pgn.headers['Black'] = str(engine2)
    result = board.result()

    movetimes = {str(engine1): avg_mvtime_eng1, str(engine2): avg_mvtime_eng2}
    return pgn, result, movetimes


import random 
def random_search_algorithm(board: chess.Board, evaluate_board) -> chess.Move:
    return random.choice(list(board.legal_moves))

if __name__ == "__main__":
    # Here you can write your own and point to it as such
    my_search_algorithm = alpha_beta_search # NOTE: CHANGE THIS TO YOUR SEARCH ALGORITHM, IF YOU HAVE WRITEN ONE
    my_eval_function = simple_board_eval     # NOTE: CHANGE THIS TO YOUR EVALUATION FUNCTION, IF YOU HAVE WRITEN ONE
    my_engine1 = create_engine_class(my_eval_function, my_search_algorithm, 'MyName', 123456)()

    opponent_engine = create_engine_class(simple_board_eval, random_search_algorithm, 'OpponentName', 654321)()

    # NOTE, if you would like to play as black , then switch the engines in play_game()
    pgn, result, movetimes = play_game(my_engine1, opponent_engine)
    print(pgn) # Copy the output in the terminal and paste it into https://lichess.org/paste to view the game
    print('\nMy average move time: ', movetimes[str(my_engine1)])
    # NOTE: If you change the depth parameter in the alpha_beta_search function, you can see how the move times change. 
    # e.g., depth=3 should be ~0.05, depth=4 ~0.3 etc.
