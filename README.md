## Problem
Sudoku is a logic-based number placement puzzle played on a 9×9 grid, which is further
divided into nine 3×3 subgrids. The objective is to fill the grid so that every row, every column,
and every 3×3 subgrid contains all digits from 1 to 9 exactly once.
The puzzle usually begins with some cells already filled with numbers, and the challenge is to
complete the remaining empty cells following the given rules: (1) no duplicate numbers in any
row, (2) no duplicate numbers in any column, (3) no duplicate numbers in any 3×3 subgrid.
Sudoku represents a well-defined problem with clear rules and a single or unique solution in
most cases. However, the number of possible configurations is extremely large, which makes
solving Sudoku computationally challenging, especially when many cells are left empty at the
start.

## Challenges
In solving Sudoku, there are several main challenges. During the search process, there are
a vast number of possible number configurations, making exhaustive exploration highly
inefficient due to the enormous search space. In addition, when many cells are still empty, the
algorithm must make early guesses without knowing whether those guesses will lead to a valid
solution or not, which can trigger very deep backtracking. Another challenge is maintaining
consistency across rows, columns, and 3×3 subgrids simultaneously, which increases the
complexity of constraint propagation. Finally, designing an algorithm that balances accuracy,
efficiency, and the ability to handle various difficulty levels requires the proper use of heuristics
to reduce the search space effectively.

## Backtracking Flowchart:
<img width="1242" height="594" alt="Screenshot 2025-10-16 102300" src="https://github.com/user-attachments/assets/f5383f8c-4919-4265-87f5-e8a68d496706" />
How the backtracking algorithm works on a high level is that for each empty cell, the code inserts a value
of k from 1 to 9 and test one by one whether the value works or not. It does this by validating whether k is
valid or not for that cell number, and if it isn’t valid, then it moves on to the next k value. But if it is valid,
then it will recursively call the solve() function. If the solve() recursion fails, it means that somewhere
along the line, there are no valid solutions. If this happens, then the algorithm backtracks to the current
cell, and resets the k value. It will then check the next k value for the current cell. This process will repeat
until a valid solution is found.

## MRV x Naked-Pairs Hybrid Heuristics Flowchart:
<img width="1594" height="554" alt="Screenshot 2025-10-16 102335" src="https://github.com/user-attachments/assets/ae7e9136-3e7e-4769-9bcd-5ab8b55ce27a" />
Meanwhile for the hybrid heuristics algorithm, we modified the original backtracking algorithm by
implementing the method of MRV (Minimum Reduced Values) and Naked-Pairs before running the
backtracking function.


How the algorithm works is as follows:
1. determines the possible candidates of each cell
2. filters the naked pairs in each cell
3. sorts the cells based on the least number of candidates
4. If 2 cells have a tie (same number of candidates), then the cell with the lower row index is
prioritized, and if they have the same row index, then the cell with the lower column value is
prioritized

List of heuristics strategies used:
1. MRV: Prioritizing cells with the fewest candidates
2. Naked Pairs: If in a row, column, or grid there exists 2 cells with the same exact 2 candidates
(pairs), then eliminate the values a and b in all other cells within that row/column/grid

(Notes: prioritize naked pairs first, then if a cell doesn't have naked pairs but has a shared value with
another cell, use simple elimination. If no shared values exist, then no need for elimination of any kind.)





