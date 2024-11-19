import chess

def evaluate_board(board: chess.Board) -> float:
    return 0


if __name__ == "__main__":
    board = chess.Board("r1bqk2r/2pp1ppp/p1n2n2/1p2p3/1b2P3/1B1P1N2/PPP2PPP/RNBQ1RK1 b kq - 0 7")
    print(board)
    print(evaluate_board(board))
