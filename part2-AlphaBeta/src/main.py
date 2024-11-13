from alphabeta import TicTacToe
from alphabeta import alpha_beta_value

from random import randint


def play(state, user_input=False):
    """Makes turn and prints the result of it until the game is over
    :param state: The initial state of the game (TicTacToe)
    """
    i=0
    while not state.is_end_state():
        (c := "x") if state.crosses_turn else (c := "o")

        if user_input:
            print(state)
            move_index = int(input(f"({c}) Enter a num from 1-9: ")) - 1
        else:
            print(state)
            move_index = i
            i += 1

        state.move(move_index, c)
        state.crosses_turn = not state.crosses_turn

        state.generate_children()
        print(alpha_beta_value(state))


def main():
    """You need to implement the following functions/methods:
    play(state): makes turn and prints the result of it until the game is over
    value() in TicTacToe class: returns the current score of the game
    generate_children() in TicTacToe class: returns a list of all possible states after this turn
    alpha_beta_value(node): implements the MinMax algorithm with alpha-beta pruning
    max_value(node, alpha, beta): implements the MinMax algorithm with alpha-beta pruning
    min_value(node, alpha, beta):implements the MinMax algorithm with alpha-beta pruning
    """
    empty_board = 3 * '???'
    state = TicTacToe(empty_board, True)
    play(state, False)


if __name__ == '__main__':
    main()
