import copy
import random
import math

class TicTacToeGame:
    def __init__(self,initial_state=['']*9,turn=0):
        self.initial_turn = turn
        self.initial_state = initial_state
    def __str__(self):
        return str(self.initial_state)
    def actions(self,state):
        #To reduce complexity, the starting state is picked using random and not by min_max
        if state == ['']*9:
            return [math.floor(random.random()*9)]
        else:
            return [i for i,v in enumerate(state) if v == '']
    def result(self,state,move):
        result_state = copy.deepcopy(state)
        result_state[move[0]] = 'X' if move[1] == 0 else 'O'
        return result_state
    def update(self,move):
        self.initial_state[move[0]] = 'X' if move[1] == 0 else 'O'
    def utility(self, state, inverted=False):
        result = self._utility(state)
        return abs(result-1) if inverted == True and result != None else result
    def _utility(self, state):
        result = 0
        #Check rows
        for i in range(0,8,3):
            if state[i] == state[i+1] == state[i+2] and state[i] in ['X','O']:
                return 1 if state[i] == 'X' else 0
        #Check diagonals
        for i in range(3):
            if state[i] == state[i+3] == state[i+6] and state[i] in ['X','O']:
                return 1 if state[i] == 'X' else 0
        #Check diagonals
        if state[0] == state[4] == state[8] and state[0] in ('X', 'O'):
            return 1 if state[0] == 'X' else 0
        elif state[2] == state[4] == state[6] and state[2] in ('X', 'O'):
            return 1 if state[2] == 'X' else 0
        elif '' not in state:
            return .5
        else:
            return None
    def is_done(self, state):
        u = self.utility(state)
        if u == 0 or u == 1 or u ==.5:
            return True
        else:
            return False
    def display_state(self, state=None):
        if state == None:
            state = self.initial_state
        for i in range(0,8,3):
            print("|",end='')
            for item in state[i:i + 3]:
                print(f"{item:>1}|",end='')
            print("")
        print("")
    def reset(self):
        self.initial_state = ['']*9

def test_is_done():
    state1 = ['']*9 #Should return False
    state2 = ['X']*9 #Should return True
    state3 = ['O']*9 #Should return True
    state4 = ['O']*8 + [''] #Should return True
    state5 = ['X','O','X','O','X','X','O','X','O'] #Should return True
    state6 = ['O' if i % 3 != 2 else '' for i in range(9)] #Should return True
    state7 = ['X' if not i > 5 else '' for i in range(9)] #Should return True
    state8 = ['' if i not in [0,4,8] else 'O' for i in range(9)] #Should return False
    state9 = ['' if i not in [2,4,6] else 'X' for i in range(9)] #Should return True
    state10 = ['X' if i in [3,5] else 'O' if i not in [1,4,7] else '' for i in range(9)] #Should return True
    states = [(state1, False), (state2,True), (state3,True), (state4,True),(state5,True),
              (state6,True), (state7,True), (state8,True), (state9,True), (state10,False)]

    game = TicTacToeGame()
    for i,(state,test) in enumerate(states):
        print(f"game.is_done(state{i+1}) -> {game.is_done(state)} #Should return {test}")
def test_utility():
    state1 = ['']*9 #Should return False
    state2 = ['X']*9 #Should return True
    state3 = ['O']*9 #Should return True
    state4 = ['O']*8 + [''] #Should return False
    state5 = ['X','O','X','O','X','X','O','X','O'] #Should return True
    state6 = ['O' if i % 3 != 2 else '' for i in range(9)] #Should return False
    state7 = ['X' if not i > 5 else '' for i in range(9)] #Should return False
    state8 = ['' if i not in [0,4,8] else 'O' for i in range(9)] #Should return True
    state9 = ['' if i not in [2,4,6] else 'X' for i in range(9)] #Should return True
    state10 = ['' if i not in [1,4,7] else 'O' for i in range(9)] #Should return True
    states = [(state1, None), (state2,1), (state3,0), (state4,0),(state5,.5),
              (state6,0), (state7,1), (state8,0), (state9,1), (state10,0)]

    game = TicTacToeGame()
    for i,(state,test) in enumerate(states):
        print(f"game.utility(state{i+1}) -> {game.utility(state)} #Should return {test}")

def minimax_search(game):
    def utility(state):
        return game.utility(state, inverted=game.initial_turn==1)
    def _max_search(game,state,turn, depth):
        if game.is_done(state):
            return utility(state)-depth*.001, (None,turn)
        else:
            best = [-float('inf'),(None,turn)]
            for a in game.actions(state):
                v,move = _min_search(game,game.result(state,(a,turn)),(turn+1)%2, depth+1)
                if v > best[0]:
                    best = [v,(a,turn)]
            return best
    def _min_search(game,state,turn, depth):
        if game.is_done(state):
            return utility(state)+depth*.001 ,(None,turn)
        else:
            best = [float('inf'),(None,turn)]
            for a in game.actions(state):
                v,move = _max_search(game,game.result(state,(a,turn)),(turn+1)%2, depth+1)
                if v < best[0]:
                    best = [v,(a,turn)]
            return best

    return _max_search(game,game.initial_state,game.initial_turn, 0)

if __name__ == "__main__":
    game = TicTacToeGame(turn=0)
    play_again = True
    iterations = 0
    playerScore,botScore = 0,0
    while True:
        game.reset()
        print("")
        player = iterations%2
        turn = 0

        if player == 0:
            game.display_state()
            print("You go first as X")
        else:
            print("I'll go first as X\n")
        while not game.is_done(game.initial_state):
            if player == 0:
                game.initial_turn = turn
                nMove = int(input("Your turn: "))
                while True:
                    if game.initial_state[nMove] != '':
                        print("That move is not available.")
                        nMove = int(input("Your turn (be careful!): "))
                    if game.initial_state[nMove] == '':
                        break
                game.update((nMove,turn))
            else:
                game.initial_turn = turn
                game.update(minimax_search(game)[1])

            game.display_state()

            turn = (turn+1) % 2
            player = (player+1) % 2

        game.display_state()
        winner = game.utility(game.initial_state)
        if winner == 1 and iterations%2 == 0:
            print("Congratulations, you won.")
            playerScore = playerScore + 1
        elif winner == 1 and iterations%2 == 1:
            print("I won!!!!")
            botScore = botScore + 1
        elif winner == 0 and iterations%2 == 0:
            print("I won as O, thats amazing!!!!")
            botScore = botScore + 1
        elif winner == 0 and iterations%2 == 1:
            print("Congratulations, you won.")
            playerScore = playerScore + 1
        else:
            print("Darn, its a Cat's game!!!")

        play_again = input("\nWould you like to play again [y/n]?: ")
        if play_again != 'y' and play_again != 'Y':
            break
        print(f"\nScore: you have {playerScore} and I have5 {botScore}")
        player = (player+1) %2
        iterations = iterations + 1

    print("Au revoir my favorite nemesis!")