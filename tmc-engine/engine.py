import chess
from chess.engine import PlayResult
from ..homemade import ExampleEngine
from ..lib.types import MOVE, HOMEMADE_ARGS_TYPE
from search import alpha_beta_search

class TmcEngine(ExampleEngine):
    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        pass
