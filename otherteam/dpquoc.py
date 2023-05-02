#from OthelloPlayer import AlphaBetaPlayer
#from OthelloBoard import OthelloBoard
import time, copy, threading

class OthelloState():
    
    def __init__(self, board, current_player, is_max_player, parent = None, from_action = None):
        self.current_player = current_player
        self.board = board
        self.is_max_player = is_max_player
        self.parent = parent
        self.from_action = from_action
        self.children = []
        
    def get_children(self):
        moves = self.board.get_legal_moves(self.current_player)
        for move in moves:
            new_board = copy.deepcopy(self.board)
            new_board.execute_move(move, self.current_player)
            child_state = OthelloState(new_board,-self.current_player, not self.is_max_player, self, move)
            
            # Append the child state to the list of children
            self.children.append(child_state)
        return self.children
    
    def evaluate(self):
        if self.is_max_player:
            return self.board.evaluate(self.current_player)
        else:
            return self.board.evaluate(-self.current_player)

class AlphaBetaPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        min_depth = 2
        max_depth = 5
        start_time = time.time()
        init_state = OthelloState(board, current_player, True)

        results = {}
        threads = []
        for depth in range(min_depth, max_depth + 1):
            t = threading.Thread(target=self.run_alphabeta, args=(init_state, depth, results, start_time))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
            
        for depth in range(max_depth, min_depth - 1, -1):
            best_child = results[depth]
            if best_child != "Out of time":
                # print(depth)
                if best_child == None:
                    return None
                return best_child.from_action
            
        
    
    def run_alphabeta(self, state, depth, results, start_time):
        value, best_child = self.alphabeta(copy.deepcopy(state), depth, float('-inf'), float('inf'), True, start_time)
        results[depth] = best_child
        
    def alphabeta(self, state, depth, alpha, beta, maximizing_player, start_time):
        if time.time() - start_time >= 2.8 :
            return -123456 , "Out of time"
        
        if depth == 0:
            return state.evaluate(), None
        state.get_children()
        if len(state.children) == 0:
            return state.evaluate(), None

        if maximizing_player:
            best_child = None
            value = float('-inf')
            for child in state.children:
                child_value, _ = self.alphabeta(child, depth - 1, alpha, beta, False, start_time)
                
                if child_value == -123456 :
                    return -123456 , "Out of time"
                
                if child_value > value:
                    value = child_value
                    best_child = child
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_child
        else:
            best_child = None
            value = float('inf')
            for child in state.children:
                child_value, _ = self.alphabeta(child, depth - 1, alpha, beta, True, start_time)
                if child_value == -123456 :
                    return -123456 , "Out of time"
                if child_value < value:
                    value = child_value
                    best_child = child
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, best_child

import numpy as np

class OthelloBoard():
    
    # list of all 8 directions on the board, as (x,y) offsets
    directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
    board_size = 8
    
    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.board = np.array(initial_state, dtype=np.int8)
        else:
            self.board = np.zeros((self.board_size, self.board_size), dtype=np.int8)
            # Set the initial four cells
            center = self.board_size // 2
            self.board[center - 1:center + 1, center - 1:center + 1] = np.array([[-1, 1], [1, -1]], dtype=np.int8)
        
        
    def get_legal_moves(self, player):
        opponent = -player
        
        # create an array of all cells where the player has a piece
        player_cells = np.where(self.board == player, 1, 0)
        
        # create an array of all cells where the opponent has a piece
        opponent_cells = np.where(self.board == opponent, 1, 0)
        
        # create an array of all cells that are empty
        empty_cells = np.where(self.board == 0, 1, 0)
       
        legal_moves = []
        # check all directions for each player piece
        for r, c in zip(*np.where(player_cells)):
            for dr, dc in OthelloBoard.directions:
                r2, c2 = r + dr, c + dc
                if (r2 < 0 or r2 >= self.board_size or c2 < 0 or c2 >= self.board_size or 
                    player_cells[r2, c2] or not opponent_cells[r2, c2]):
                    continue
                # found a potential legal move, keep following the direction
                while True:
                    r2, c2 = r2 + dr, c2 + dc
                    if r2 < 0 or r2 >= self.board_size or c2 < 0 or c2 >= self.board_size:
                        break
                    if empty_cells[r2, c2]:
                        legal_moves.append((r2, c2))
                        break
                    if player_cells[r2, c2]:
                        break
                        
        return legal_moves

    def execute_move(self, move, player):
        # opponent = -player
        
        # create an array of all cells where the player has a piece
        player_cells = np.where(self.board == player, 1, 0)

        # # create an array of all cells where the opponent has a piece
        # opponent_cells = np.where(self.board == opponent, 1, 0)

        # create an array of all cells that are empty
        empty_cells = np.where(self.board == 0, 1, 0)

        # update the new board with the new piece
        r, c = move
        self.board[r][c] = player

        # flip opponent pieces as necessary
        for dr, dc in OthelloBoard.directions:
            r2, c2 = r + dr, c + dc
            if (r2 < 0 or r2 >= self.board_size or c2 < 0 or c2 >= self.board_size or
                    empty_cells[r2][c2] or player_cells[r2][c2]):
                continue
            # found a line of opponent pieces to flip
            to_flip = [(r2, c2)]
            while True:
                r2 += dr
                c2 += dc
                if (r2 < 0 or r2 >= self.board_size or c2 < 0 or c2 >= self.board_size or
                        empty_cells[r2][c2]):
                    break
                if player_cells[r2][c2]:
                    for fr, fc in to_flip:
                        self.board[fr][fc] = player
                    break
                to_flip.append((r2, c2))

        return self.board

    def evaluate(self, player):
        opponent = -player
        
        player_count = np.sum(self.board == player)
        opponent_count = np.sum(self.board == opponent)
        
        # calculate the coin parity heuristic value
        coin_parity_value = 100 * (player_count - opponent_count) / (player_count + opponent_count)
        
        # calculate the corner heuristic value
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        max_corner_value = 0
        min_corner_value = 0
        
        for corner in corners:
            if self.board[corner] == player:
                max_corner_value += 1
            elif self.board[corner] == opponent:
                min_corner_value += 1
        
        if (max_corner_value + min_corner_value) != 0:
            corner_heuristic_value = 100 * (max_corner_value - min_corner_value) / (max_corner_value + min_corner_value)
        else:
            corner_heuristic_value = 0
            
        return coin_parity_value + corner_heuristic_value


    
    def print_board(self):
        print("    ", end="")
        for i in range(self.board_size):
            print(i, end=" ")
        print()
        print("   +" + "--" * self.board_size + "+")
        for i in range(self.board_size):
            print(i, "|", end=" ")
            for j in range(self.board_size):
                if self.board[i][j] == 1:
                    print("X", end=" ")
                elif self.board[i][j] == -1:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            print("|", i)
        print("   +" + "--" * self.board_size + "+")
        print("    ", end="")
        for i in range(self.board_size):
            print(i, end=" ")
        print()

# board = OthelloBoard()
# board.print_board()
# print(board.get_legal_moves(1))
# print(board.execute_move((2,3), 1))


def select_move(cur_state, player_to_move, remain_time):
    return AlphaBetaPlayer().play(OthelloBoard(cur_state), player_to_move, remain_time)