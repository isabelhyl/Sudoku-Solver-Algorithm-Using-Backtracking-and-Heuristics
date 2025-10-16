import time

# cell validation function
def is_valid(grid, row, col, k):
    # check row
    if k in grid[row]:
        return False
    
    # check column
    for i in range(9):
        if grid[i][col] == k:
            return False
    
    # check box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == k:
                return False
    
    return True 

# solver function
def solve(grid, row=0, col=0):
    if row == 9:
        return True
    if col == 9:
        return solve(grid, row + 1, 0)
    if grid[row][col] != 0:
        return solve(grid, row, col + 1)

    for k in range(1, 10): 
        if is_valid(grid, row, col, k):
            grid[row][col] = k
            if solve(grid, row, col + 1):
                return True
            grid[row][col] = 0  # reset

    return False

# main program
print("Enter your Sudoku puzzle (9 lines, 9 numbers each, 0 for empty):")
grid = []

for _ in range(9):
    row = list(map(int, input().split()))
    grid.append(row)

# start_time = time.perf_counter()

print("\nSolving Sudoku...\n")
if solve(grid):
    print("Solved Sudoku:")
    for row in grid:
        print(*row)
else:
    print("No solution exists.")

# end_time = time.perf_counter()
# elapsed_time = end_time - start_time
# print(f"\nElapsed time: {elapsed_time:.6f} seconds")



# TEST CASES: easy (berhasil), intermediate (berhasil), difficult, not fun (masing2 satu)

