from ballsort_utils import *
from queue import Queue, PriorityQueue

def bfs_ball_sort(state, max_capacity=-1):
    '''
    BFS search. Will always find the optimal solution but is very slow.
    '''
    # if a max capacity is not specified, assume that one of the tubes are full
    if max_capacity == -1:
        max_capacity = max(len(i) for i in state)

    # initialize search
    q = Queue()
    seen = set()
    state = tuple_form(state)
    key = tuple(sorted(state))
    q.put((state, []))
    seen.add(key)

    while not q.empty():
        state, path = q.get()

        for i in range(len(state)):
            for j in range(len(state)):
                if i == j:  # useless move
                    continue
                # make all legal moves
                if state[i] and len(state[j]) < max_capacity:
                    new_state = move(state, i, j)
                    key = tuple(sorted(state))
                    if key not in seen:
                        seen.add(key)
                        new_path = path + [(i, j)]
                        if solved(new_state):
                            return new_path
                        q.put((new_state, new_path))
    return []


def bfs_sort_color_rule(state, max_capacity=-1):
    '''
    bfs search, assuming that we are only allowed to make moves if it follows the following rule:
    you may only move a ball to a tube that is empty or has the same color ball on top.
    '''
    # if a max capacity is not specified, assume that one of the tubes are full
    if max_capacity == -1:
        max_capacity = max(len(i) for i in state)

    q = Queue()
    seen = set()
    state = tuple_form(state)
    q.put((state, []))
    key = tuple(sorted(state))
    seen.add(key)

    while not q.empty():
        state, path = q.get()
        for i in range(len(state)):
            for j in range(len(state)):
                if i == j:
                    continue
                # make all legal moves
                if state[i] and len(state[j]) < max_capacity and (not state[j] or state[i][-1] == state[j][-1]):
                    new_state = move(state, i, j)
                    key = tuple(sorted(new_state))
                    if key not in seen:
                        seen.add(key)
                        new_path = path + [(i, j)]
                        if solved(new_state):
                            return new_path
                        q.put((new_state, new_path))
    return []


def semi_bfs_ball_sort(state, max_capacity=-1):
    '''
    BFS search on moves that follow the color rule first, followed by a BFS search on moves that
    do not follow the color rule. Returns the first solution it finds.
    '''
    # if a max capacity is not specified, assume that one of the tubes are full
    if max_capacity == -1:
        max_capacity = max(len(i) for i in state)

    # initialize search
    q = Queue()
    non_cr_q = Queue()
    seen = set()
    state = tuple_form(state)
    q.put((state, []))
    seen.add(state)

    while not q.empty() or not non_cr_q.empty():
        state, path = non_cr_q.get() if q.empty() else q.get()

        for i in range(len(state)):
            for j in range(len(state)):
                if i == j:  # useless move
                    continue
                # make all legal moves
                if state[i] and len(state[j]) < max_capacity:
                    new_state = move(state, i, j)
                    key = tuple(sorted(new_state))
                    if key not in seen:
                        seen.add(key)
                        new_path = path + [(i, j)]
                        if solved(new_state):
                            return new_path
                        
                        if not state[j] or state[i][-1] == state[j][-1]:
                            q.put((new_state, new_path))
                        else:
                            non_cr_q.put((new_state, new_path))
    return []


"""
In addition to the heuristic passed into h_ball_sort, which just evaluates the state,
this function also evaluates a heuristic based on moves. It turns out that following the 
color rule is actually a really good heuristic so this functions prioritizes that heuristic
first.
"""

def h_ball_sort(state, max_capacity=-1, heuristic=mono_color):
    """
    Search using a heuristics and priority queue to determine where to search next.
    Does not find the optimal solution but it is much faster than bfs.
    heuristic: Evaluation of a current state. Lower is better
    """
    # if a max capacity is not specified, assume that one of the tubes are full
    if max_capacity == -1:
        max_capacity = max(len(i) for i in state)

    min_steps = min_solution(state)

    q = PriorityQueue()
    v = set()
    state = tuple_form(state)
    key = tuple(sorted(state))  # we do not care about optimal solution so tube order does not matter
    q.put((0, 0, state, []))  # (color rule heuristic, heuristic, state, solution)
    v.add(key)

    while not q.empty():
        _, __, state, path = q.get()
        for i in range(len(state)):
            for j in range(len(state)):
                if i == j:  # useless move
                    continue
                # make all other legal moves
                if state[i] and len(state[j]) < max_capacity:
                    new_state = move(state, i, j)
                    key = tuple(sorted(new_state))
                    if key not in v:
                        v.add(key)
                        new_path = path + [(i, j)]
                        # don't bother checking if the game is solved unless it has made enough moves
                        if len(new_path) >= min_steps and solved(new_state):
                            return new_path
                        # only add to queue if the potential solution would be short enough.
                        h = heuristic(new_state)
                        color_rule = 0 if (not state[j] or state[i][-1] == state[j][-1]) else 1  # 0 takes priority
                        q.put((color_rule, h, new_state, new_path))
    return []

"""
h_ball_sort_color_rule ends up being much faster because making moves takes up a lot of time.
A lot of time is saved by just not making moves that do not follow the color rule.
"""

def h_ball_sort_color_rule(state, max_capacity=-1, heuristic=mono_color):
    """
    Same as h_ball_sort, but assumes that only moves that follow the color rule are legal
    """
    # if a max capacity is not specified, assume that one of the tubes are full
    if max_capacity == -1:
        max_capacity = max(len(i) for i in state)

    min_steps = min_solution(state)

    q = PriorityQueue()
    v = set()
    state = tuple_form(state)
    key = tuple(sorted(state))  # we do not care about optimal solution so tube order does not matter
    q.put((0, state, []))  # (heuristic, state, solution)
    v.add(key)

    while not q.empty():
        _, state, path = q.get()
        for i in range(len(state)):
            for j in range(len(state)):
                if i == j:  # useless move
                    continue
                # make all other legal moves
                if state[i] and len(state[j]) < max_capacity and (not state[j] or state[i][-1] == state[j][-1]):
                    new_state = move(state, i, j)
                    key = tuple(sorted(new_state))
                    if key not in v:
                        v.add(key)
                        new_path = path + [(i, j)]
                        # don't bother checking if the game is solved unless it has made enough moves
                        if len(new_path) >= min_steps and solved(new_state):
                            return new_path
                        # only add to queue if the potential solution would be short enough.
                        h = heuristic(new_state)
                        q.put((h, new_state, new_path))
    return []