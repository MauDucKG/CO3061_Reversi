import time

def select_move(cur_state, player_to_move, remain_time):
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

    def evaluate_final(board):
        total_tile = 0
        for row in board:
            for tile in row:
                total_tile += tile

        if total_tile > 0:
            return 10000 + total_tile
        elif total_tile < 0:
            return -10000 + total_tile
        else:
            return 0

    def evaluate_corner(board, player_to_move = 0):
    
        """POINT_TABLE_0 = [[1000, -100,  1,  1,  1,  1, -100, 1000],
                        [-100, -100, -1, -1, -1, -1, -100, -100],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [-100, -100, -1, -1, -1, -1, -100, -100],
                        [1000, -100,  1,  1,  1,  1, -100, 1000]]
        
        POINT_TABLE_1 = [[1000, -100,  1,  1,  1,  1, -100, 1000],
                        [-100, -100, -1, -1, -1, -1, -100, -100],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [-100, -100, -1, -1, -1, -1, -100, -100],
                        [1000, -100,  1,  1,  1,  1, -100, 1000]]"""
        
        """POINT_TABLE_0 = [[1000,    1,  1,  1,  1,  1,    1, 1000],
                        [   1, -100, -1, -1, -1, -1, -100,    1],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [   1, -100, -1, -1, -1, -1, -100,    1],
                        [1000,    1,  1,  1,  1,  1,    1, 1000]]
        
        POINT_TABLE_1 = [[1000,    1,  1,  1,  1,  1,    1, 1000],
                        [   1, -100, -1, -1, -1, -1, -100,    1],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [   1, -100, -1, -1, -1, -1, -100,    1],
                        [1000,    1,  1,  1,  1,  1,    1, 1000]]"""

        POINT_TABLE_0 = [[ 100, -100,  1,  1,  1,  1, -100,  100],
                        [-100, -100, -1, -1, -1, -1, -100, -100],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [-100, -100, -1, -1, -1, -1, -100, -100],
                        [ 100, -100,  1,  1,  1,  1, -100,  100]]
        
        POINT_TABLE_1 = [[ 100, -100,  1,  1,  1,  1, -100,  100],
                        [-100, -100, -1, -1, -1, -1, -100, -100],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1, -1,  1,  1, -1,   -1,    1],
                        [   1,   -1,  1, -1, -1,  1,   -1,    1],
                        [-100, -100, -1, -1, -1, -1, -100, -100],
                        [ 100, -100,  1,  1,  1,  1, -100,  100]]

        score = 0
        total_tile = 0
        num_tile = 0

        if board[0][0] != 0:
            if board[0][0] == -1:
                POINT_TABLE_0[0][1] = 100
                POINT_TABLE_1[0][1] = 1

                POINT_TABLE_0[1][0] = 100
                POINT_TABLE_1[1][0] = 1

                POINT_TABLE_0[1][1] = 1
                POINT_TABLE_1[1][1] = 1
            elif board[0][0] == 1:
                POINT_TABLE_0[0][1] = 1
                POINT_TABLE_1[0][1] = 100

                POINT_TABLE_0[1][0] = 1
                POINT_TABLE_1[1][0] = 100

                POINT_TABLE_0[1][1] = 1
                POINT_TABLE_1[1][1] = 1

        if board[0][7] != 0:
            if board[0][7] == -1:
                POINT_TABLE_0[0][6] = 100
                POINT_TABLE_1[0][6] = 1

                POINT_TABLE_0[1][7] = 100
                POINT_TABLE_1[1][7] = 1

                POINT_TABLE_0[1][6] = 1
                POINT_TABLE_1[1][6] = 1
            elif board[0][7] == 1:
                POINT_TABLE_0[0][6] = 1
                POINT_TABLE_1[0][6] = 100

                POINT_TABLE_0[1][7] = 1
                POINT_TABLE_1[1][7] = 100

                POINT_TABLE_0[1][6] = 1
                POINT_TABLE_1[1][6] = 1

        if board[7][0] != 0:
            if board[7][0] == -1:
                POINT_TABLE_0[6][0] = 100
                POINT_TABLE_1[6][0] = 1

                POINT_TABLE_0[7][1] = 100
                POINT_TABLE_1[7][1] = 1

                POINT_TABLE_0[6][1] = 1
                POINT_TABLE_1[6][1] = 1
            elif board[7][0] == 1:
                POINT_TABLE_0[6][0] = 1
                POINT_TABLE_1[6][0] = 100

                POINT_TABLE_0[7][1] = 1
                POINT_TABLE_1[7][1] = 100

                POINT_TABLE_0[6][1] = 1
                POINT_TABLE_1[6][1] = 1

        if board[7][7] != 0:
            if board[7][7] == -1:
                POINT_TABLE_0[6][7] = 100
                POINT_TABLE_1[6][7] = 1

                POINT_TABLE_0[7][6] = 100
                POINT_TABLE_1[7][6] = 1

                POINT_TABLE_0[6][6] = 1
                POINT_TABLE_1[6][6] = 1
            elif board[0][0] == 1:
                POINT_TABLE_0[6][7] = 1
                POINT_TABLE_1[6][7] = 100

                POINT_TABLE_0[7][6] = 1
                POINT_TABLE_1[7][6] = 100

                POINT_TABLE_0[6][6] = 1
                POINT_TABLE_1[6][6] = 1

        for i, row in enumerate(board):
            for j, tile in enumerate(row):
                total_tile += tile
                if tile == -1:
                    num_tile += 1
                    score += tile*POINT_TABLE_0[i][j]
                elif tile == 1:
                    num_tile += 1
                    score += tile*POINT_TABLE_1[i][j]
        return score + 3*total_tile/(65 - num_tile)

    def minimax(cur_state, player_to_move, time_limit, alpha, beta, eval_func, no_legal = False):
        
        start_time = time.perf_counter()
        
        # minimax algorithm
        if time_limit <= 0.005:
            #print("time limit is: ", time_limit)
            time_amount = time.perf_counter() - start_time
            time_spare = 0 if time_amount > time_limit else time_limit - time_amount
            #print("time spare evaluate: ", time_spare)
            return None, eval_func(cur_state, player_to_move), 0

        legal_moves = get_legal_moves(cur_state, player_to_move)

        if len(legal_moves) == 0:
            if no_legal:
                time_amount = time.perf_counter() - start_time
                time_spare = 0 if time_amount > time_limit else time_limit - time_amount
                #print("time spare no more step: ", time_spare)
                return None, evaluate_final(cur_state), time_spare
            else:
                #time_limit -= time.perf_counter() - start_time
                return minimax(cur_state, -player_to_move, time_limit, alpha, beta, eval_func, True)

        #time_limit -= time.perf_counter() - start_time
        #print("time limit for node is: ", time_limit)
        time_slot = time_limit/len(legal_moves)
        #print("time limit divide by ", len(legal_moves), ", time slot is: ", time_slot)

        best_move = None

        if player_to_move == 1:        
            max_value = float('-inf')
            for i, move in enumerate(legal_moves):
                new_state = make_move(cur_state, move, player_to_move)
                _, value, time_spare = minimax(new_state, -player_to_move, time_slot, alpha, beta, eval_func)
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
            for i, move in enumerate(legal_moves):
                new_state = make_move(cur_state, move, player_to_move)
                _, value, time_spare = minimax(new_state, -player_to_move, time_slot, alpha, beta, eval_func)
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


    time_limit = 2.8
    if remain_time < 3:
        time_limit = 0.5  
    move, _, timespare = minimax(cur_state, player_to_move, time_limit, float('-inf'), float('inf'), evaluate_corner)
    #print("TIME SPARE TOTAL: ", timespare)
    return move
