# Ball Sort Solver
This python script contains various algorithms that solve the popular mobile game "Ball Sort Puzzle" by Voodoo. The solution is returned as a list of tuples, where a tuple (x, y) means to move a ball from tube x to tube y.

## What is the Color Rule?
In some variations of the game, you are only allowed to move a ball from one tube to another if the destination tube is empty or the top ball in that tube is the same color as the one you are moving.

## Sort Types

`bfs_ball_sort` Pure bfs sort that will always find the optimal solution

`bfs_sort_color_rule` Pure bfs sort that assuming you need to follow the color rule

`semi_bfs_ball_sort` Performs a bfs sort on all moves that follow the color rule, followed by all the moves that do not.

`h_ball_sort` Uses a heuristic search to find a solution much faster (10-100x) but will not always find the optimal solution

`h_ball_sort_color_rule` Uses a heruistic search but assumes you need to follow the color rule

- Color rule sorting is *much* faster than bfs sorting, and also makes a good heruistic even if the puzzle is not solvable when the color rule present. `h_ball_sort` will automatically use that heuristic in addition to whatever heuristic you give it.

- Benchmarks for these sorts can be seen in `ball_sort_test.py`

## How to Use
You can use the script by importing functions from the ballsortsolver.py file in your Python code.

The puzzle format is `List[List[int]])` and the solution is in the format `List[Tuple[int, int]]`. Every color should be assigned a number and the list is bottom to top. For example, `[0, 0, 0, 1]` might represent a tube of 3 red balls with a blue ball on the top.

The function returns a list of tuples, where a tuple (x, y) means to move a ball from tube x to tube y.

Here's an example of how to use the solve_ball_sort_puzzle() function:

```python
from ballsortsolver import bfs_sort_color_rule, print_solution

puzzle = [[0, 3, 2, 2], [3, 4, 1, 3], [1, 1, 0, 3], [4, 4, 1, 4], [2, 2, 0, 0], [], []]
solution = bfs_sort_color_rule(puzzle)
print_solution(solution)
```

```
# Output
Move ball from tube 1 to tube 5
Move ball from tube 2 to tube 5
Move ball from tube 2 to tube 6
Move ball from tube 1 to tube 2
Move ball from tube 3 to tube 1
Move ball from tube 3 to tube 2
Move ball from tube 1 to tube 3
Move ball from tube 1 to tube 3
Move ball from tube 1 to tube 5
Move ball from tube 4 to tube 6
Move ball from tube 4 to tube 6
Move ball from tube 0 to tube 4
Move ball from tube 0 to tube 4
Move ball from tube 0 to tube 5
Move ball from tube 0 to tube 6
```
