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


def check_constraints(a, b, num, grid, constraints):

    #check row and col num uniqueness
    for x in range (grid.shape[0]):
        if grid[a, x] == num or grid[x, b] == num:
            return False

    #check for adjacency constraints
    up = grid[a-1, b] if a-1 >= 0 else 0
    left = grid[a, b-1] if b-1 >= 0 else 0
    right = grid[a, b+1] if b+1 < grid.shape[0] else 0
    down = grid[a+1, b] if a+1 < grid.shape[0] else 0

    if down != 0 and (a, b, True) in constraints and abs(num-down) != 1:
        return False
    elif down != 0 and (a,b,True) not in constraints and abs(num-down) == 1:
        return False

    if up != 0 and (a-1, b, True) in constraints and abs(num-up) != 1:
        return False
    elif up != 0 and (a-1,b,True) not in constraints and abs(num-up) == 1:
        return False
    
    if right != 0 and (a, b, False) in constraints and abs(num-right) != 1:
        return False
    elif right != 0 and (a,b,False) not in constraints and abs(num-right) == 1:
        return False

    if left != 0 and (a, b-1, False) in constraints and abs(num-left) != 1:
        return False
    elif left != 0 and (a,b-1,False) not in constraints and abs(num-left) == 1:  
        return False
    
    return True

            
def solve(grid, constraints, row, col):
    if (row+1, col) == grid.shape: 
        return grid

    elif col == grid.shape[1]:
        return solve(grid, constraints, row+1, 0)
    
    elif grid[row, col] != 0: 
        return solve(grid, constraints, row, col+1)

    for num in range(1, grid.shape[0]+1):
        print(row, col, num)
        if check_constraints(row, col, num, grid, constraints):
            
            grid[row, col] = num
            s = solve(grid, constraints, row, col+1) 
            if s is None: 
                grid[row, col] = 0
                continue
            else: return s
    
    return None
            

        
def solve_renzoku(grid, constraints):
    return [solve(grid, constraints, 0, 0)]

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


"""test_grid = np.asarray([[0, 0, 3], [3, 0, 0], [0, 0, 0]])
test_constraints = set([(0,0,False), (0,0,True), (0,1,True), (1,0,False), (1,1,False), (1,1,True), (1,2,True), (2,1,False)])
print_renzoku(test_grid, test_constraints)
test_renzoku(test_grid, test_constraints)"""

ar = np.asarray([[0, 0, 0, 0], [0, 0, 0, 0], [3, 0, 0, 0], [0, 0, 0, 0]])
csr = set([(0,1,False),(0,2,True),(0,2,False),(0,3,True),(1,1,False),(1,2,False),(2,0,True),(2,0,False), (2,1,True),(2,1,False),(3,0,False),(3,1,False)])
print_renzoku(ar, csr)
test_renzoku(ar, csr)