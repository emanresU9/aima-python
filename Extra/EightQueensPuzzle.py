import random
import math
from typing import List
import copy

class Eight_Queens():
    def get_random_configurations(self, many):
        configs = [[math.floor(random.random()*8) for i in range(8)] for _ in range(many)]
        return configs
    def value(self,state:List[int]):
        total = 0
        total += sum(state[col1] == state[col2] for col1 in range(len(state)) for col2 in range(col1+1,len(state)))
        total += sum((state[col1] == state[col2] - (col1-col2)) or (state[col1] == state[col2] + (col1-col2)) for col1 in range(len(state)) for col2 in range(col1+1,len(state)))
        return -1*total
    def result(self,state:List[int],move):
        state = copy.deepcopy(state)
        state[move[0]] = move[1]
        return state
    def neighbors(self,state:List[int]):
        return [self.result(state,(i,setting)) for i in range(8) for setting in range(8) if setting != state[i]]

def hill_climb_queens_search(queens):
    iterations = 50
    states = queens.get_random_configurations(10)
    while iterations:
        #go through each table in states and update it with its best neightbor
        # if its value is less, or restart if its value is value is less than
        # any of the other states.
        for i,state in enumerate(states):
            best = max(queens.neighbors(state), key=lambda node: queens.value(node))
            if queens.value(best) > queens.value(state):
                states[i] = best
            #Else check if the state is less than the max valued state in states
            elif queens.value(state) < queens.value(max(states,key=lambda node: queens.value(node))):
                states[i] = queens.get_random_configurations(1)[0]
            if queens.value(state) == 0:
                return state
        iterations -= 1
    return max(states,key=lambda node: queens.value(node))

queens = Eight_Queens()
res = hill_climb_queens_search(queens)
print(f"{res} value: {queens.value(res)}")