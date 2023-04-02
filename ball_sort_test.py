from ballsortsolver import *
from time import perf_counter

# ball sort functions to be tested:
# bfs_ball_sort, bfs_sort_color_rule, semi_bfs_ball_sort
TEST_SORTS = [bfs_sort_color_rule, h_ball_sort, h_ball_sort_color_rule]

def time_sorts(puzzle, sorts=TEST_SORTS):
    for f in sorts:
        start = perf_counter()
        solution = f(puzzle)
        end = perf_counter() - start
        print(f'{f.__name__} found a {len(solution)}{"(already solved or no solution)" if not len(solution) else ""} step solution in {round(end*1000, 2)}ms.')


if __name__ == "__main__":
    # This puzzle is impossible if you are only allowed to place balls on the same color or an empty tube.
    impossible_color_rule = [[6, 1, 5, 4], [9, 1, 9, 2], [0, 6, 7, 8], [4, 0, 2, 1], [4, 0, 7, 3], [0, 8, 6, 1], [5, 4, 3, 5], [9, 3, 5, 7], [8, 8, 2, 3], [7, 6, 2, 9], []]
    # This puzzle is possible to solve only using moves that follow the color rule
    possible_color_rule = [[6, 9, 2, 8], [4, 2, 1, 2], [8, 0, 9, 6], [4, 0, 1, 5], [0, 1, 3, 8], [9, 0, 7, 4], [8, 3, 7, 3], [6, 5, 5, 9], [6, 5, 2, 7], [4, 7, 3, 1], [], []]

    print('Non-color rule puzzle:')
    time_sorts(impossible_color_rule)

    print('\nColor rule puzzle')
    time_sorts(possible_color_rule)

    print('\nRandom puzzle (11 colors, 14 tubes [11 full and 3 empty], max capacity 4)')
    state = random_state(11, 3, 4)
    time_sorts(state, TEST_SORTS[1:])
