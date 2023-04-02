from random import shuffle
from ballsort import Puzzle

def random_puzzle(full_tubes, empty_tubes, capacity):
    '''
    Generate a random puxxle
    '''
    return Puzzle(random_state(full_tubes, empty_tubes, capacity), capacity)

def random_state(full_tubes, empty_tubes, capacity):
    '''
    Generate a random puxxle
    '''
    state = [i for _ in range(capacity) for i in range(full_tubes)]
    shuffle(state)
    return [state[i:i+capacity] for i in range(0, len(state), capacity)] + [[] for _ in range(empty_tubes)]

def tuple_form(state) -> tuple:
    """
    Turns a list of lists of numbers to a tuple of tuples of numbers. This is so states can be added to a set
    """
    return tuple(map(tuple, state))

def solved(state) -> bool:
    """
    Checks if the puzzle is solved. A puzzle is considered solved if each tube
    has one or less colors. Note that this means that 4 tubes with one blue ball each
    is just as solved as 1 tube with 4 blue balls and 3 empty tubes.
    """
    for tube in state:
        if len(set(tube)) > 1:
            return False
    return True

def min_solution(state):
    """
    A minimum bound for number of steps needed to solve the puzzle
    """
    steps = 0
    for tube in state:
        if tube:
            for i in tube[1:]:
                if i != tube[0]:
                    steps += 1
    return steps

def move(state, i, j):
    """
    Return a new state if you moved the top ball from tube i to tube j
    """
    # remove top ball from i
    # add that ball to j
    # don't change any other tube
    return tuple(state[i][:len(state[i])-1] if k == i\
                else state[j]+state[i][-1::] if k == j\
                else state[k]\
                for k in range(len(state)))

# HEURISTICS

def mono_color(state):
    """
    A heuristic determined by how many different colors are in each tube.
    The lower the value, the closer to the solution.
    """
    return sum(len(set(i)) for i in state)

def consecutive_colors(state):
    """
    A heuristic determined by how many of the same color are next to each other.
    """
    res = 0
    for tube in state:
        for i in range(1, len(tube)):
            if tube[i] == tube[i-1]:
                res -= 1  # lower heuristic is better
    return res
