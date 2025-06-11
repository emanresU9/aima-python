import math
from typing import List
import queue
import pickle
import os
import time

class X_Puzzle:
    def __init__(self, state=None, puzzle_size=None):
        if puzzle_size is None:
            puzzle_size = 8
        if state is None:
            state = [num for num in range(puzzle_size)]
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
        new_state = list(state)
        blank = new_state.index(0)
        new_state[action],new_state[blank] = new_state[blank],new_state[action]
        return tuple(new_state)

    def create_tile_sets(self, sig_chars=4):
        tile_count = sig_chars - 1
        state = [num for num in range(1, self.size)] + [0]
        tile_sets = []
        for i in range(self.size // tile_count):
            current_set = [-1] * tile_count * i
            if (i + 1) * tile_count - self.size == 0:
                current_set += state[i * tile_count:]
            else:
                current_set += state[tile_count * i:tile_count * (i + 1)] + [-1] * (self.size - tile_count * (i + 1) - 1) + [
                    0]
            tile_sets.append(tuple(current_set))
        if self.size % tile_count > 1:
            last_set = [-1] * (self.size // tile_count) * tile_count + state[tile_count * (self.size // tile_count):self.size - 1]
            tile_sets.append(tuple(last_set))
        return tuple(tile_sets)

    def create_databases(self):
        tile_sets = self.create_tile_sets()
        databases = {tile_set:{} for tile_set in tile_sets}
        for i,tile_set in enumerate(tile_sets):
            if os.path.exists(f"{self.size}_puzzle_set_{i}.db"):
                databases[tile_set] = self.read_db_from_file(f"{self.size}_puzzle_set_{i}.db")
            else:
                databases[tile_set] = self.DepthFirstSearch(tile_set)
                self.send_db_to_file(databases[tile_set],f"{self.size}_puzzle_set_{i}.db")
        return databases

    def send_db_to_file(self, database, filename):
        with open(filename, "wb") as fd:
            pickle.dump(database, fd)

    def read_db_from_file(self,filename):
        with open(filename, 'rb') as fd:
            database = pickle.load(fd)
        return database or None


    def IDS_DB_Create(self, tile_set, max_db_size=None):

        def check_add_state(node,database):
            state = tuple(node["state"])
            if state in database:
                return False
            else:
                database[state] = node["depth"]
                return True

        def DLS(puzzle, node, database, limit):
            if check_add_state(node, database):
                if len(database) == max_db_size:
                    return "success"
            if limit > 0:
                actions = puzzle.action_list(node['state'])
                if len(actions) == 0:
                    return "failure"
                failure = True
                for a in actions:
                    next = dict(state=puzzle.result(node['state'],a), depth=node['depth']+1)
                    result = DLS(puzzle, next, database, limit-1)
                    if result == "success":
                        return "success"
                    if result != "failure":
                        failure = False
                if failure:
                    return "failure"
            return "limit"

        significant_charaters = len([i for i in tile_set if i != -1])
        if max_db_size is None:
            max_db_size = math.prod([i for i in range(len(tile_set), len(tile_set) - significant_charaters, -1)])
        puzzle = X_Puzzle(tile_set) #contains transition model methods on the tile_set
        database = {}
        limit = 0
        node = dict(state=tile_set,depth=0)
        while True:
            result = DLS(puzzle, node, database, limit)
            print(f"limit={limit} and db_size={len(database)}")
            if result == "success":
                break
            elif result == "failure":
                break
            else:
                limit += 1
        return database

    def DepthFirstSearch(self, tile_set, max_db_size=None):
        def check_add_state(node,database):
            state = tuple(node["state"])
            if state in database:
                return False
            else:
                database[state] = node["depth"]
                return True

        current_depth = 0
        significant_charaters = len([i for i in tile_set if i != -1])
        if max_db_size is None:
            max_db_size = math.prod([i for i in range(len(tile_set), len(tile_set) - significant_charaters, -1)])
        puzzle = X_Puzzle(tile_set)
        first_node = {"state":tile_set, "depth":0}
        frontier = [first_node]
        database = {}
        while len(frontier) != 0:
            node = frontier.pop()
            if node['depth'] > current_depth:
                current_depth +=1
                print(f"depth={current_depth} and nodes={len(database)}")
            actions = puzzle.action_list(node['state'])
            if len(actions) != 0:
                for a in actions:
                    new_node = dict(state=puzzle.result(node['state'],a), depth=node['depth']+1)
                    if check_add_state(new_node, database):
                        if len(database) >= max_db_size:
                            break
                        frontier.append(new_node)
        return database

def create_databases(puzzle_size):
    puzzle = X_Puzzle(puzzle_size=puzzle_size)
    databases = puzzle.create_databases()

if __name__ == "__main__":
    start = time.time()

    puzzle = X_Puzzle(puzzle_size=9)
    tile_set = puzzle.create_tile_sets()[0]
    print(tile_set)
    db = puzzle.DepthFirstSearch(tile_set)
    # print(db.items())
    end = time.time()
    print(f"Elapsed Time: {end-start:.4f}")