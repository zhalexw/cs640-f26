"""Strongly solve the noisy tic-tac-toe game in tictactoe.py.

Run ``python solve.py`` to write one row per nonterminal board to solution.tsv.
Board indices use tictactoe.encode_board. Moves use the zero-based (i, j)
coordinates accepted by tictactoe.move_board.
"""

from decimal import Decimal
from functools import cache
from fractions import Fraction
from pathlib import Path

import numpy as np

from tictactoe import decode_board, won_board


BOARD_COUNT = 3**9
PLACE_VALUES = tuple(3**cell for cell in range(9))


@cache
def solve_board(board_index: int) -> tuple[Fraction, tuple[int, ...]]:
    """Return optimal expected reward and all maximizing moves for this board.

    The reward is from the perspective of the side whose turn is determined by
    the number of occupied cells. Terminal positions have no legal moves.
    """
    if not 0 <= board_index < BOARD_COUNT:
        raise ValueError("board_index must be between 0 and 3**9 - 1")

    board = decode_board(board_index)
    occupied = int(np.count_nonzero(board))
    current_player = 1 + occupied % 2
    winner = won_board(board)
    if winner is not None:
        return Fraction(1 if winner == current_player else -1), ()
    if occupied == 9:
        return Fraction(0), ()

    best_value: Fraction | None = None
    best_moves: list[int] = []
    for cell in range(9):
        if board.flat[cell] != 0:
            continue

        # The next side to move is the opponent, so negate each child's value.
        own_mark = board_index + current_player * PLACE_VALUES[cell]
        other_mark = board_index + (3 - current_player) * PLACE_VALUES[cell]
        move_value = -(3 * solve_board(own_mark)[0]
                       + solve_board(other_mark)[0]) / 4

        if best_value is None or move_value > best_value:
            best_value = move_value
            best_moves = [cell]
        elif move_value == best_value:
            best_moves.append(cell)

    assert best_value is not None
    return best_value, tuple(best_moves)


def write_solution(path: Path) -> int:
    """Write all nonterminal positions and return the number of rows."""
    count = 0
    with path.open("w", encoding="utf-8", newline="") as output:
        output.write("board_index\tbest_move_i\tbest_move_j\texpected_reward\n")
        for board_index in range(BOARD_COUNT):
            value, moves = solve_board(board_index)
            if not moves:
                continue
            move = moves[0]  # Deterministic tie break: smallest row-major cell.
            reward = Decimal(value.numerator) / Decimal(value.denominator)
            output.write(
                f"{board_index}\t{move // 3}\t{move % 3}\t{reward:f}\n"
            )
            count += 1
    return count


if __name__ == "__main__":
    destination = Path(__file__).with_name("solution.tsv")
    count = write_solution(destination)
    value, moves = solve_board(0)
    print(f"Wrote {count} positions to {destination}")
    print(f"Empty board: best moves {moves}, expected reward {value} ({float(value):.10f})")
