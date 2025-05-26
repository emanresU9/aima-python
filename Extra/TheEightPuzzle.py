# To solve the eight puzzle we need
# nodes, a problem, and a search strategy.

import math
from search import *

goal = [1,2,3,4,5,6,7,8,0]
init = (2, 4, 3, 1, 5, 6, 7, 8, 0)

# Heuristics for 8 Puzzle Problem
def manhattan(node):
    state = node.state
    index_goal = {0: [2, 2], 1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1]}
    index_state = {}
    index = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
    x, y = 0, 0

    for i in range(len(state)):
        index_state[state[i]] = index[i]

    mhd = 0

    for i in range(8):
        for j in range(2):
            mhd = abs(index_goal[i][j] - index_state[i][j]) + mhd

    return mhd

eightPuzzle = EightPuzzle(init)
assert eightPuzzle.check_solvability(init)
recursive_best_first_search(eightPuzzle,manhattan).solution()

