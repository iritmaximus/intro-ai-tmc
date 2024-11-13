from collections import deque
from copy import copy
from math import inf

TEMPLATE_FIELD = '|e|e|e|\n|e|e|e|\n|e|e|e|\n'
HUGE_NUMBER = 1000000


class AlphaBetaNode(object):
    def __init__(self):
        pass

    def generate_children(self):
        pass

    def is_max_node(self):
        pass

    def is_end_state(self):
        pass

    def value(self):
        pass


class TicTacToe(AlphaBetaNode):
    """Class that contains current state of the game and implements AlphaBetaNode methods
    :attr state: Current state of the board (str)
    :attr state: Indicates whose turn it is (Boolean)

    Board is implemented as a string of 9 chars, numbered like this:

    |1|2|3|
    |4|5|6|
    |7|8|9|
    """

    def __init__(self, state, crosses_turn):
        super().__init__()
        self.state = state
        self.crosses_turn = crosses_turn

    def is_end_state(self):
        return ('?' not in self.state) or self.won('x') or self.won('o')

    def won(self, c):
        triples = [self.state[0:3], self.state[3:6], self.state[6:9], self.state[::3], self.state[1::3],
                   self.state[2::3], self.state[0] + self.state[4] + self.state[8],
                   self.state[2] + self.state[4] + self.state[6]]
        combo = 3 * c
        return combo in triples

    def move(self, index: int, char: str):
        if index > 8:
            raise IndexError("Max index can be 8, was", index)
        if char.lower() not in ["x", "o"]:
            raise ValueError("Incorrect character", char)
        if self.state[index] in ["x", "o"]:
            raise ValueError("Trying to rewrite existing move (", self.state[index], ") at index", index, "with", char)

        self.state = replace_string_at_index(self.state, index, char)

    def get_current_player_char(self):
        # walrus operator, very cool.
        (c := "x") if self.crosses_turn else (c := "o")
        return c

    def get_state(self):
        return self.state

    def __str__(self):
        field = TEMPLATE_FIELD
        for c in self.state:
            field = field.replace('e', c, 1)

        return field

    def is_max_node(self):
        return self.crosses_turn

    def generate_children(self, depth=0):
        """
        Generates list of all possible states after this turn
        :return: list of TicTacToe objects
        """
        game_queue = deque([copy(self)])
        unique_states = set()

        while game_queue:
            game = game_queue.popleft()
            state = game.get_state()
            c = game.get_current_player_char()


            i=0
            while (index := state.find("?", i)) != -1:
                new_state = replace_string_at_index(state, index, c)
                i+=1

                if new_state in unique_states: continue
                unique_states.add(new_state)

                new_game = copy(game)
                new_game.state = new_state
                new_game.crosses_turn = not new_game.crosses_turn

                game_queue.append(new_game)
                # print("child state (", i, ", ", c, "):\n", str(new_game), sep="")

            if depth <= 0:
                return unique_states

            depth -= 1

        return 

    def value(self):
        """
        Current score of the game (0, 1, -1)
        :return: int
        """
    
        if self.won("x"):
            return 1
        if self.won("o"):
            return -1
        if "?" not in self.state:
            return 0

        print("OH NO, the weird state:\n", str(self), sep="")
        return None

def replace_string_at_index(string: str, index: int, char: str):
    return string[:index] + char + string[index+1:]


def alpha_beta_value(node):
    """Implements the MinMax algorithm with alpha-beta pruning
    :param node: State of the game (TicTacToe)
    :return: int
    """

    if node.crosses_turn:
        return max_value(node)
    return min_value(node)


def max_value(node, alpha=-inf, beta=inf):
    if node.is_end_state(): 
        return node.value()
    value = -inf

    for new_node in node.generate_children():
        value = max(value, min_value(TicTacToe(new_node, False), alpha, beta))
        alpha = max(value, alpha)

        if alpha >= beta:
            return value

    return value


def min_value(node, alpha=-inf, beta=inf):
    if node.is_end_state(): 
        return node.value()
    value = inf

    for new_node in node.generate_children():
        value = min(value, max_value(TicTacToe(new_node, True), alpha, beta))
        beta = min(value, beta)

        if alpha >= beta:
            return value

    return value
