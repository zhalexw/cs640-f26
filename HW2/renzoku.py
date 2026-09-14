import numpy as np

def render_renzoku(grid, constraints):
    assert len(grid.shape) == 2
    (m, n) = grid.shape

    # grid

    output = [None for _ in range(2 * m + 1)]

    for i in range(m + 1):
        output[2 * i] = ['+', '-'] * n + ['+']

    for i in range(m):
        output[2 * i + 1] = ['|', ' '] * n + ['|']

    # numbers

    for i in range(m):
        for j in range(n):
            if grid[i, j] != 0:
                output[2 * i + 1][2 * j + 1] = str(grid[i, j])

    # constraints

    for (i, j, v_h) in constraints:
        if v_h:
            output[2 * i + 2][2 * j + 1] = '●'
        else:
            output[2 * i + 1][2 * j + 2] = '●'

    # flatten to string

    output = [''.join(row) for row in output]
    output = '\n'.join(output)

    return output

def print_renzoku(grid, constraints):
    print(render_renzoku(grid, constraints))


def check_constraints(a, b, grid, constraints):

    cur = grid[a, b]
    right = grid[i, j+1] if j+1 < grid.shape[1] else -1
    down = grid[i+1, j] if i+1 < grid.shape[0] else -1

    for (i, j, v_h) in constraints:
        if i==a and j==b:
            if v_h and abs(cur-right)==1: return True
            elif (not v_h) and abs(cur-down)==1: return True
            else: return False


def solve_renzoku(grid, constraints):
    return


def solve(grid, constraints, row, col):
    if (row+1, col) == grid.shape: 
        return

    elif col == grid.shape[1]:
        return solve(grid, constraints, row+1, 0)
    
    elif grid[row, col] != 0: 
        return solve(grid, constraints, row, col+1)

    for num in range(1, grid.shape[0]):
        
                    
#true = 3●2
#false = 3
        #●
        #2

def test_renzoku(grid, constraints):
    solutions = solve_renzoku(grid, constraints)
    if solutions is None:
        print("solve_renzoku returned None")
        return
    if len(solutions) == 0:
        print("solve_renzoku returned no solutions")
        return

    for (i, solution) in enumerate(solutions):
        print(f"Solution {0}:")
        print_renzoku(solution, constraints)


test_grid = np.asarray([[0, 3, 2], [3, 2, 0], [0, 0, 0]])
test_constraints = set([(0, 1, False), (0, 1, True), (0, 2, True), (1, 0, False), (1, 0, True), (1, 1, False), (1, 1, True), (2, 0, False)])
print_renzoku(test_grid, test_constraints)
test_renzoku(test_grid, test_constraints)