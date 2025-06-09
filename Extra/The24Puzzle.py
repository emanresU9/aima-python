import math
from typing import List

class X_Puzzle:
    def __init__(self, state):
        assert math.sqrt(len(state)) - math.floor(math.sqrt(len(state))) == 0, "len(state) not a square"
        self.initial = state
        self.side_len = int(math.sqrt(len(state)))
        self.size = len(self.initial)
        self.blank = self.blank_space()
    @staticmethod
    def generate_random_state(side_len):
        return [num for num in range(1,side_len**2)] + [0]
    def blank_space(self):
        return self.initial.index(0)
    def set_state(self, state):
        assert math.sqrt(len(state)) - math.floor(math.sqrt(len(state))) == 0, "len(state) not a square"
        self.initial = state
        self.side_len = int(math.sqrt(len(state)))
        self.size = len(self.initial)
        self.blank = self.blank_space()
    def action_list(self, state:List[int]):
        blank = state.index(0)
        actions = []
        if blank%self.side_len != 0:
            actions.append(blank-1)
        if blank%self.side_len != self.side_len-1:
            actions.append(blank+1)
        if blank >= self.side_len:
            actions.append(blank-self.side_len)
        if blank < self.size - self.side_len:
            actions.append(blank+self.side_len)
        return actions
    def result(self, state, action):
        blank = state.index(0)
        state[action],state[blank] = state[blank],state[action]
        return state
    def create_database(self):
        state = [num for num in range(1,self.size)] + [0]
        tile_sets = [[-1]*set_count*4 + state[set_count*4:(set_count+1)*4]+[-1]*(len(state)-(set_count+1)*4) for set_count in range(math.floor(self.size/4))]
        for i in range(len(tile_sets)):
            tile_sets[i][-1] = 0

        databases = {tile_set:{} for tile_set in tile_sets}
        for tile_set in tile_sets:
            databases[tile_set] = IDFS_DB_Create(tile_set)


def IDFS_DB_Create(tile_set):
    database = {tile_set:0}
    limit = 1


puzzle = X_Puzzle([num for num in range(1,16)] + [0])
state = puzzle.initial
