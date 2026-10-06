"""Property checks for the exhaustive noisy tic-tac-toe solution."""

import csv
import unittest
from fractions import Fraction
from pathlib import Path

import numpy as np

from solve import BOARD_COUNT, solve_board
from tictactoe import decode_board, encode_board, won_board


class SolverTests(unittest.TestCase):
    def test_last_move_can_win_for_either_player(self):
        board = np.array([[1, 1, 0],
                          [2, 2, 1],
                          [2, 1, 2]], dtype=np.int32)
        # Player 1 wins the top row with probability 3/4; player 2 wins
        # the opposite diagonal with probability 1/4.
        self.assertEqual(solve_board(int(encode_board(board))),
                         (Fraction(1, 2), (2,)))

    def test_solution_table_is_complete_and_legal(self):
        path = Path(__file__).with_name("solution.tsv")
        with path.open(encoding="utf-8", newline="") as source:
            reader = csv.DictReader(source, delimiter="\t")
            self.assertEqual(reader.fieldnames,
                             ["board_index", "best_move_i", "best_move_j",
                              "expected_reward"])
            rows = list(reader)
        by_index = {int(row["board_index"]): row for row in rows}
        self.assertEqual(len(rows), len(by_index))

        for index in range(BOARD_COUNT):
            board = decode_board(index)
            value, moves = solve_board(index)
            expected_moves = bool(np.any(board == 0) and won_board(board) is None)
            self.assertEqual(bool(moves), expected_moves, index)
            self.assertEqual(index in by_index, expected_moves, index)
            self.assertTrue(Fraction(-1) <= value <= Fraction(1))
            if not moves:
                continue

            row = by_index[index]
            self.assertEqual((int(row["best_move_i"]), int(row["best_move_j"])),
                             divmod(moves[0], 3))
            self.assertEqual(Fraction(row["expected_reward"]), value)
            self.assertTrue(all(board.flat[move] == 0 for move in moves))

    def test_rotation_and_reflection_preserve_optimal_play(self):
        cells = np.arange(9).reshape(3, 3)
        for transform in (np.rot90, np.fliplr):
            transformed_cells = transform(cells)
            old_to_new = tuple(int(np.flatnonzero(transformed_cells == cell)[0])
                               for cell in range(9))
            for index in range(BOARD_COUNT):
                value, moves = solve_board(index)
                if not moves:
                    continue
                transformed_index = int(encode_board(transform(decode_board(index))))
                transformed_value, transformed_moves = solve_board(transformed_index)
                self.assertEqual(value, transformed_value, index)
                self.assertEqual({old_to_new[move] for move in moves},
                                 set(transformed_moves), index)


if __name__ == "__main__":
    unittest.main()
