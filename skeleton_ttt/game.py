from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="red"),
)


class Game:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        """Return all possible winning combinations, i.e. rows, columns and diagonals."""
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        # TODO: check that the current move has not been played already 
        # and that there is no winner yet. Note that non-played cells
        # contain an empty string (i.e. ""). 
        # Use variables no_winner and move_not_played.
        no_winner = True
        move_not_played = False
        if row < 0 or col < 0 or row > BOARD_SIZE or col > BOARD_SIZE : move_not_played = True
        for mvS in self._current_moves:
            for mv in mvS:
                if mv.row == move.row and mv.col == move.col and mv.label == move.label : move_not_played = True 
        if move.label == "" : move_not_played = True
        if self.current_player.label != move.label : move_not_played = True
        no_winner = not self.has_winner()
        return no_winner and not move_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        self._has_winner = self.has_winner()

        for combo in self._winning_combos:
            if (row, col) in combo:
                is_winning = True
                for mv in combo:
                    label = self._current_moves[mv[0]][mv[1]].label
                    if label != move.label:
                        is_winning = False
                        break
                if is_winning:
                    self.winner_combo = combo
                    return

        # TODO: check whether the current move leads to a winning combo.
        # Do not return any values but set variables  self._has_winner 
        # and self.winner_combo in case of winning combo.
        # Hint: you can scan pre-computed winning combos in self._winning_combos


    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        for combo in self._winning_combos:
            old_label = None
            is_equal = True
            for move in combo:
                label = self._current_moves[move[0]][move[1]].label
                if(old_label is None):
                    old_label = label
                    continue
                if("" == label):
                    is_equal = False
                    break
                if(old_label != label):
                    is_equal = False
                    break
            if(is_equal):
                return True
        return False

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        # TODO: check whether a tie was reached.
        # There is no winner and all moves have been tried.
        if not(self.has_winner()):
            for row, row_content in enumerate(self._current_moves):
                for col, _ in enumerate(row_content):
                    if(row_content[col].label == ""):
                        return False
            return True
        else:
            return False

    def toggle_player(self):
        """Return a toggled player."""
        try:
            self.current_player = next(self._players)
        except StopIteration as err:
            print(f"Unexpected {err=}, {type(err)=}")
       
    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []