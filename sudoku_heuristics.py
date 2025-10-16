# MRV-Naked Pairs hybrid heuristics algorithm

# how the code works:
# 1. determines the possible candidates of each cell
# 2. filter the naked pairs in each cell
# 3. sorts the cells based on the least amount of candidates
# 4. if 2 cells have a tie (same amount of candidates), then the cell with the lower row indexes is prioritized, and if they have the same row, then the cell with the lower column value is prioritized


# list of heuristics strategies:
# 1. mrv -> prioritizing cells with the least candidates
# 2. naked pairs -> if in a row, column, or grid there exists 2 cells with the same exact 2 candidates (pairs), then eliminate the values a and b in all other cells within that row/column/grid
# notes: prioritize naked pairs first, then if a cell doesnt have naked pairs but has a shared value as another cell, then use simple elimination. If no shared values exist, then no need for elimination of any kind



import heapq
from dataclasses import dataclass, field
from typing import List, Set, Tuple, Optional

Sudoku = List[List[int]]

@dataclass(order=True)
class Node:
    length: int
    domain: Set[int] = field(compare=False)
    indices: Tuple[int, int] = field(compare=False)

# calculating the domain of the cell candidates
def domain(board: Sudoku, i: int, j: int) -> Set[int]:
    full_domain = set(range(1, 10))
    row = set(board[i])
    col = {board[n][j] for n in range(9)}
    row_start, col_start = (i // 3) * 3, (j // 3) * 3
    grid = {board[row_start + a][col_start + b] for a in range(3) for b in range(3)}
    return full_domain.difference(row | col | grid)
    # row | col | grid --> union of row, col, and grid
    # full_domain (universe set) - row,col,grid union = the set of possible candidates for the cell

# check if cell is valid
def validate(board: Sudoku, i: int, j: int, x: int) -> bool:
    for n in range(9):
        if board[i][n] == x or board[n][j] == x:
            return False
    row = (i // 3) * 3
    column = (j // 3) * 3
    for r in range(row, row + 3):
        for c in range(column, column + 3):
            if board[r][c] == x:
                return False
    return True

def solved(board: Sudoku) -> bool:
    return all(all(cell != 0 for cell in row) for row in board)


def eliminate_naked_pairs(cells, domains, row=None, col=None, grid=False):
    # look for pairs
    seen = {}
    for idx, d in cells:
        d_tuple = tuple(sorted(d))
        if d_tuple in seen:
            first_idx = seen[d_tuple]
            second_idx = idx
            # eliminate the pair values from all other cells in the same row/column/grid
            pair_values = set(d_tuple)
            if row is not None:
                for j in range(9):
                    if j != first_idx and j != second_idx:
                        domains[row][j] -= pair_values
            elif col is not None:
                for i in range(9):
                    if i != first_idx and i != second_idx:
                        domains[i][col] -= pair_values
            elif grid:
                r0, c0 = first_idx
                r1, c1 = second_idx
                box_row = (r0 // 3) * 3
                box_col = (c0 // 3) * 3
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        if (r, c) != (r0, c0) and (r, c) != (r1, c1):
                            domains[r][c] -= pair_values
        else:
            seen[d_tuple] = idx
            
# naked pairs elimination
# can only work if the domain length is exactly 2, because we're sorting out the duplicate pairs
def naked_pairs(domains: List[List[Set[int]]]) -> None:
    for i in range(9):
        row_cells = [(j, domains[i][j]) for j in range(9) if len(domains[i][j]) == 2] 
        eliminate_naked_pairs(row_cells, domains, row=i)
        col_cells = [(j, domains[j][i]) for j in range(9) if len(domains[j][i]) == 2]
        eliminate_naked_pairs(col_cells, domains, col=i)
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            grid_cells = []
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    if len(domains[r][c]) == 2:
                        grid_cells.append(((r, c), domains[r][c]))
            eliminate_naked_pairs(grid_cells, domains, grid=True)

def compute_domains(board: Sudoku) -> List[List[Set[int]]]:
    domains = [[domain(board, i, j) if board[i][j] == 0 else set() for j in range(9)] for i in range(9)]
    naked_pairs(domains)
    return domains

def mrv_indices(board: Sudoku) -> Optional[Tuple[int, int, Set[int]]]:
    domains = compute_domains(board)
    heap = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                d = domains[i][j]
                if not d:
                    return (i, j, d)
                heapq.heappush(heap, Node(len(d), d, (i, j)))
    if not heap:
        return None
    node = heapq.heappop(heap)
    return (node.indices[0], node.indices[1], node.domain)

def backtrack(board: Sudoku) -> bool:
    if solved(board):
        return True

    mrv = mrv_indices(board)
    if mrv is None:
        return True  # solved
    i, j, d = mrv
    if not d:
        return False

    for x in sorted(d):
        if validate(board, i, j, x):
            board[i][j] = x
            if backtrack(board):
                return True
            board[i][j] = 0
    return False

# main program
print("Enter your Sudoku puzzle (9 lines, 9 numbers each, 0 for empty):")
grid: Sudoku = [list(map(int, input().split())) for _ in range(9)]

print("\nSolving Sudoku...\n")
if backtrack(grid):
    print("Solved Sudoku:")
    for row in grid:
        print(*row)
else:
    print("No solution exists.")
