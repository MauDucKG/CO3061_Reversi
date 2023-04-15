
import random as rd
import time

def select_move(cur_state, player_to_move, remain_time):
    def minimax(cur_state, player_to_move, time_limit, alpha, beta, no_legal = False):
        MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
                    (0, -1),           (0, +1),
                    (+1, -1), (+1, 0), (+1, +1)]

        def has_tile_to_flip(board, move, direction, player_to_move):
            i = 1
            if player_to_move in (-1, 1) and is_valid_coord(move[0], move[1]):
                curr_tile = player_to_move
                while True:
                    row = move[0] + direction[0] * i
                    col = move[1] + direction[1] * i
                    if not is_valid_coord(row, col) or board[row][col] == 0:
                        return False
                    elif board[row][col] == curr_tile:
                        break
                    else:
                        i += 1
                return i > 1

        def make_move(board, move, player_to_move):
            new_board = [row.copy() for row in board]
            new_board[move[0]][move[1]] = player_to_move

            for direction in MOVE_DIRS:
                if has_tile_to_flip(new_board, move, direction, player_to_move):
                    row, col = move[0] + direction[0], move[1] + direction[1]
                    while new_board[row][col] == -player_to_move:
                        new_board[row][col] = player_to_move
                        row += direction[0]
                        col += direction[1]
            return new_board

        def is_valid_coord(row, col):
            return 0 <= row < 8 and 0 <= col < 8

        def is_legal_move(board, move, player_to_move):
            return move != () and is_valid_coord(move[0], move[1]) and board[move[0]][move[1]] == 0 and any(has_tile_to_flip(board, move, direction, player_to_move) for direction in MOVE_DIRS)

        def get_legal_moves(cur_state, player_to_move):
            return [(row, col) for row in range(8) for col in range(8) if is_legal_move(cur_state, (row, col), player_to_move)]

        def evaluate(board, player_to_move):
            #moves1 = get_legal_moves(board, player_to_move)
            #moves2 = get_legal_moves(board, -player_to_move)
            #if not moves1 and not moves2:

            point_table = [[ 8, -4,  6,  6,  6,  6, -4,  8],
                           [-4, -4, -3, -3, -3, -3, -4, -4],
                           [ 6, -3,  1,  1,  1,  1, -3,  6],
                           [ 6, -3,  1,  2,  2,  1, -3,  6],
                           [ 6, -3,  1,  2,  2,  1, -3,  6],
                           [ 6, -3,  1,  1,  1,  1, -3,  6],
                           [-4, -4, -3, -3, -3, -3, -4, -4],
                           [ 8, -4,  6,  6,  6,  6, -4,  8]]

            score = 0
            for i, row in enumerate(board):
                for j, tile in enumerate(row):
                    score += tile*point_table[i][j]
            return score
            
            #print("point: ", (len(moves1) - len(moves2))*player_to_move + 1000)
            #return (len(moves1) - len(moves2))*player_to_move + 1000



        start_time = time.perf_counter()
        
        # minimax algorithm
        if time_limit <= 0.001:
            #print("time limit is: ", time_limit)
            time_amount = time.perf_counter() - start_time
            time_spare = 0 if time_amount > time_limit else time_limit - time_amount
            #print("time spare evaluate: ", time_spare)
            return None, evaluate(cur_state, player_to_move), 0

        legal_moves = get_legal_moves(cur_state, player_to_move)

        if len(legal_moves) == 0:
            if no_legal:
                time_amount = time.perf_counter() - start_time
                time_spare = 0 if time_amount > time_limit else time_limit - time_amount
                #print("time spare no more step: ", time_spare)
                return None, evaluate(cur_state, player_to_move), time_spare
            else:
                #time_limit -= time.perf_counter() - start_time
                return minimax(cur_state, -player_to_move, time_limit, alpha, beta, True)

        #time_limit -= time.perf_counter() - start_time
        #print("time limit for node is: ", time_limit)
        time_slot = time_limit/len(legal_moves)
        #print("time limit divide by ", len(legal_moves), ", time slot is: ", time_slot)

        if player_to_move == 1:        
            max_value = float('-inf')
            best_move = None
            for i, move in enumerate(legal_moves):
                new_state = make_move(cur_state, move, player_to_move)
                _, value, time_spare = minimax(new_state, -player_to_move, time_slot, alpha, beta)
                if i + 1 < len(legal_moves):
                    time_slot += time_spare/(len(legal_moves) - (i + 1))
                if value > max_value:
                    max_value = value
                    best_move = move
                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            time_amount = time.perf_counter() - start_time
            time_spare = 0 if time_amount > time_limit else time_limit - time_amount
            #print("time spare max node: ", time_spare)
            return best_move, max_value, time_spare
        else:
            min_value = float('inf')
            best_move = None
            for i, move in enumerate(legal_moves):
                new_state = make_move(cur_state, move, player_to_move)
                _, value, time_spare = minimax(new_state, -player_to_move, time_slot, alpha, beta)
                if i + 1 < len(legal_moves):
                    time_slot += time_spare/(len(legal_moves) - (i + 1))
                if value < min_value:
                    min_value = value
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break

            time_amount = time.perf_counter() - start_time
            time_spare = 0 if time_amount > time_limit else time_limit - time_amount
            #print("time spare min node: ", time_spare)
            return best_move, min_value, time_spare

    move, _, timespare = minimax(cur_state, player_to_move, 2.8, float('-inf'), float('inf'))
    #print("TIME SPARE TOTAL: ", timespare)
    return move
