import copy
import numpy as num 
import time


#---------------------------Constant for Game Reversi---------------------------------#

EMPTY = 0
X_SIGNAL = 1
O_SIGNAL = -1
DIRECTIONS = [
    "n",
    "s",
    "w",
    "e",
    "n_w",
    "n_e",
    "s_w",
    "s_e"
]
VALID_MOVE = 2
LAST_MOVE = 3

#---------------------Define Node on GameBoard----------------------#

class GetTrack:
    def __init__(self, x= -1, y = -1, value = None):
        self.x = x 
        self.y = y 
        self.value = value

#---------------------Define The Rule and Valid move of each State----------------------#
class Problem:
    def __init__(self,n,curstate, minimax_player):
        self.n = n 
        self.board = curstate
        self.X_score = num.count_nonzero(self.board == X_SIGNAL)
        self.O_score = num.count_nonzero(self.board == O_SIGNAL)
        self.no_moves_sema = 0
        self.minimax = minimax_player
        self.last_move = None

    def move_possible(self, player_to_move): # Chỉ có thể là 1 hoặc -1
        possible_move = []
        self.board[self.board == VALID_MOVE] = EMPTY
        pieces = num.argwhere(self.board == player_to_move)
        opponent = O_SIGNAL if player_to_move == X_SIGNAL else X_SIGNAL
        for moves in pieces:
            for direction in DIRECTIONS:
                self.move_part(player_to_move, opponent, moves, direction, possible_move)
        if len(possible_move) == 0 :
            self.no_moves_sema += 1 
        else:
            self.no_moves_sema = 0
        return possible_move
    
    def invalid_move(self, x, y):
        return x < 0 or y < 0 or x >= self.n or y >= self.n

    def move_part(self, player, opponent, start, dir, moves):
        move_x = 0 
        move_y = 0 
        if dir in ("n", "n_w", "n_e"):
            move_x = -1
        elif dir in ("s", "s_w", "s_e"):
            move_x =  1
        if dir in ("w", "n_w", "s_w"):
            move_y = -1
        elif dir in ("e", "n_e", "s_e"):
            move_y = 1
        x = start[0] + move_x
        y = start[1] + move_y

        last_seen_oppo = None
        while not self.invalid_move(x,y):
            if self.board[x,y] == opponent:
                last_seen_oppo = [x,y]
            elif self.board[x,y] == player: 
                break
            elif self.board[x,y] == EMPTY:
                if last_seen_oppo is not None:
                    if not self.invalid_move(x,y):
                        self.board[x,y] = VALID_MOVE
                        moves.append((GetTrack(x,y)))
                        break
                break
            elif self.board[x,y] == VALID_MOVE:
                break
            x += move_x
            y += move_y


    def move_choosing(self, player_to_move, move):
        self.board[self.board == VALID_MOVE] = EMPTY
        self.board[move[0], move[1]] = player_to_move
        self.last_move = GetTrack(move[0], move[1])
        if player_to_move == X_SIGNAL:
            self.X_score += 1
        else:
            self.O_score += 1
        opponent = O_SIGNAL if player_to_move == X_SIGNAL else X_SIGNAL
        for direction in DIRECTIONS:
            self.movechosing_single_dir(player_to_move, opponent, move, direction) 
    

    def movechosing_single_dir(self, player, opponent, move, dir):
        move_x = 0
        move_y = 0
        if dir in ("n", "n_w", "n_s"):
            move_x = -1
        elif dir in ("s", "s_w", "s_e"):
            move_x = 1
        if dir in ("w", "n_w", "s_w"):
            move_y = -1
        elif dir in ("e", "n_e", "s_e"):
            move_y = 1

        x = move[0] + move_x
        y = move[1] + move_y

        catch_opponent= []
        while not self.invalid_move(x, y):
            if self.board[x,y] == opponent:
                catch_opponent.append([x,y])
            elif self.board[x,y] == player:
                if player == X_SIGNAL:
                    self.X_score += len(catch_opponent)
                    self.O_score -= len(catch_opponent)
                else:
                    self.X_score -= len(catch_opponent)
                    self.O_score += len(catch_opponent)
                for ele in catch_opponent:
                    self.board[ele[0],ele[1]] = player
                break
            elif self.board[x,y] == EMPTY:
                break
            x += move_x
            y += move_y   

    def status(self):
        if self.X_score == 0:
            self.O_score = self.n * self.n
            return "O is winner"
        elif self.O_score == 0:
            self.X_score = self.n * self.n
            return "X is winner"
        if self.X_score + self.O_score == self.n * self.n or self.no_moves_sema >= 2:
            if self.X_score > self.O_score:
                self.X_score = self.n * self.n - self.O_score
                return "X is winner"
            if self.O_score> self.X_score:
                self.O_score = self.n * self.n - self.X_score
                return "O is winner"
            if self.O_score == self.X_score:
                return "Equal"
        return "Ongoing"

    def simple_eval_fn(self):
        game_status = self.status()
        if game_status == "Ongoing" or game_status == "Equal":
            if self.minimax == O_SIGNAL:
                self.last_move.value = self.O_score - self.X_score
            else:
                self.last_move.value = self.X_score - self.O_score
        elif game_status == "X is winner":
            if self.minimax == X_SIGNAL:
                self.last_move.value = 100
            else:
                self.last_move.value = -100
        elif game_status == "O is winner":
            if self.minimax == O_SIGNAL:
                self.last_move.value = 100
            else:
                self.last_move.value = -100

    def advanced_eval_fn(self, player):
        moves = self.move_possible(player)
        number_of_moves = len(moves)
        if player == self.minimax:
            self.last_move.value = number_of_moves
        self.last_move.value = -number_of_moves

#---------------------Agent to findout the next node----------------------# 
        
class AI_Using:
    def __init__(self, identifier, hints, depth, evaluation_fn, move_ordering , problem:Problem, minimax_player):
        self.identifier = identifier
        self.hints = hints
        self.depth = depth
        self.evaluation_fn = evaluation_fn
        self.move_ordering = move_ordering
        self.minimax = minimax_player
        self.problem = problem


    def alpha_beta_pruning(self, problem:Problem, depth, player, opponent, alpha = float('-inf'), beta = float('inf')):
        possible_moves = problem.move_possible(player)
        if len(possible_moves) == 0 and depth == self.depth:
            return GetTrack()
        if depth == 0 or problem.status() != "Ongoing" or len(possible_moves) == 0:
            if self.evaluation_fn == "simple":
                problem.simple_eval_fn()
            else:
                problem.advanced_eval_fn(player)
            return problem.last_move
        if player == self.minimax:
            max_eval = GetTrack(value=float('-inf'))
            if self.move_ordering:
                for move in possible_moves:
                    clone = copy.deepcopy(problem)
                    clone.move_choosing(player, [move.x, move.y])
                    if self.evaluation_fn == "simple":
                        problem.simple_eval_fn()
                    else:
                        problem.advanced_eval_fn(player)
                    move.value = clone.last_move.value
                    del clone
                possible_moves = sorted(possible_moves, key=lambda x: x.value, reverse=True)
            for move in possible_moves:
                new_game = copy.deepcopy(problem)
                new_game.move_choosing(player, [move.x, move.y])
                move_evaluation = self.alpha_beta_pruning(new_game, depth - 1, opponent, player, alpha, beta)
                del new_game
                if max_eval.value < move_evaluation.value:
                    max_eval.value = move_evaluation.value
                    max_eval.x = move.x
                    max_eval.y = move.y
                alpha = max(alpha, move_evaluation.value)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = GetTrack(value=float('inf'))
            if self.move_ordering:
                for move in possible_moves:
                    clone = copy.deepcopy(problem)
                    clone.move_choosing(player, [move.x, move.y])
                    if self.evaluation_fn == "simple":
                        clone.simple_evaluation_fn()
                    else:
                        clone.advanced_evaluation_fn(player)
                    move.value = clone.last_move.value
                    del clone
                possible_moves = sorted(possible_moves, key=lambda x: x.value)
            for move in possible_moves:
                new_game = copy.deepcopy(problem)
                new_game.move_choosing(player, [move.x, move.y])
                move_evaluation = self.alpha_beta_pruning(new_game, depth - 1, opponent, player, alpha, beta)
                del new_game
                if min_eval.value > move_evaluation.value:
                    min_eval.value = move_evaluation.value
                    min_eval.x = move.x
                    min_eval.y = move.y
                beta = min(beta, move_evaluation.value)
                if beta <= alpha:
                    break
            return min_eval
        

    def result_move(self, player_to_move):
        opponent = O_SIGNAL if player_to_move == X_SIGNAL else X_SIGNAL
        start_time = time.time()
        result_move = self.alpha_beta_pruning(self.problem, self.depth, player_to_move, opponent)
        time_consumed = time.time() - start_time
        if result_move.x != -1 and result_move.y != -1:
            return result_move, time_consumed
        return None, time_consumed
    

#---------------------Running Function to find tuple for game----------------------# 

def select_move(cur_state, player_to_move, remain_time): 
    #Convert curstate into matrix
    cur_state = num.array(cur_state)
    #Calculate time
    length_board = len(cur_state)
    game = Problem(length_board, cur_state, player_to_move)
    solution = AI_Using(player_to_move, True, 5 ,'simple', False, game, player_to_move)
    result, time_consume = solution.result_move(player_to_move)
    if(result == None):
        print(f"Can't find result")
        return None
    print(f"Timecost is: {time_consume} seconds")
    if(time_consume >= 3):
        print(f"Time-consuming, {player_to_move} lose the match")
        return result.x, result.y
    remain_time -= time_consume
    if(remain_time < 0):
        print(f"Player {player_to_move} is Loser")
        return result.x, result.y
    return result.x, result.y

""" if __name__ == "__main__":
    # Input is List
    cur_state = [[0,0,0,0,0,0,0,0] for x in range(8)]
    cur_state[3][3] = 1
    cur_state[3][4] = -1
    cur_state[4][4] = 1
    cur_state[4][3] = 1 
    cur_state[5][3] = 1
    result1, result2 = select_move(cur_state, -1, 60)
    print((result1, result2)) """
   