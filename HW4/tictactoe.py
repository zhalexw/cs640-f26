import random
import numpy as np

def decode_board(board_index):
    board = np.zeros((3,3), dtype=np.int32)
    for i in range(3):
        for j in range(3):
            board[i,j] = board_index % 3
            board_index //= 3
    return board

def print_board(board):
    for i in range(3):
        print('|', end='')
        for j in range(3):
            if board[i,j] == 0:
                print(' ', end='')
            elif board[i,j] == 1:
                print('X', end='')
            else:
                print('O', end='')
        print('|')
    print()

def encode_board(board):
    board_index = 0
    for i in (2, 1, 0):
        for j in (2, 1, 0):
            board_index = board_index * 3 + board[i,j]

    return board_index

def move_board(board, i, j):
    assert board[i,j] == 0

    previous_turns = (board != 0).sum()
    side_to_move = 1 + previous_turns % 2

    new_board = board.copy()
    if random.random() < 0.75:
        new_board[i,j] = side_to_move
    else:
        new_board[i,j] = 3 - side_to_move

    return new_board

def won_board(board):
    for i in range(3):
        if np.all(board[i,:] == board[i,0]) and board[i,0] != 0:
            return board[i,0]

        if np.all(board[:,i] == board[0,i]) and board[0,i] != 0:
            return board[0,i]

    if np.all(board.diagonal() == board[0,0]) and board[0,0] != 0:
        return board[0,0]

    if np.all(board[::-1,:].diagonal() == board[2,0]) and board[2,0] != 0:
        return board[2,0]

    return None

if __name__ == "__main__":
    for i in range(5):
        print_board(decode_board(i))

    for board_index in range(3**9):
        assert encode_board(decode_board(board_index)) == board_index

    test_board = decode_board(0)
    for ply in range(9):
        test_board = move_board(test_board, ply // 3, ply % 3)
        print_board(test_board)

        winner = won_board(test_board)
        if winner is not None:
            print('Player', winner, 'won')
            break
