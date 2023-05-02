def select_move(cur_state, player_to_move, remain_time):
    def alphabeta(cur_state, depth, player_to_move, alpha = -1000, beta = 1000):
        moves = get_valid_moves(cur_state, player_to_move)
        if (len(moves) == 0): return None
        best_move = moves[0]
        for move in moves:
            newboard = cur_state.copy()
            newboard = make_move(newboard, move, player_to_move)
            score = ab_min(newboard, depth-1, player_to_move, alpha, beta)
            if score > alpha:
                alpha = score
                best_move = move
        return best_move

    def ab_min(cur_state, depth, player_to_move, alpha, beta):
        if depth == 0:
            return heuristic(cur_state, player_to_move)
        moves = get_valid_moves(cur_state, -player_to_move)
        for move in moves:
            newboard = cur_state.copy()
            newboard = make_move(newboard, move, -player_to_move)
            score = ab_max(newboard, depth-1, player_to_move, alpha, beta)
            if score < beta:
                beta = score
                best_move = move
            if alpha >= beta:
                break
        return beta

    def ab_max(cur_state, depth, player_to_move, alpha, beta):
        if depth == 0:
            
            return heuristic(cur_state, player_to_move)
        moves = get_valid_moves(cur_state, player_to_move)
        for move in moves:
            newboard = cur_state.copy()
            newboard = make_move(newboard, move, player_to_move)
            score = ab_min(newboard, depth-1, player_to_move, alpha, beta)
            if score > alpha:
                alpha = score
                best_move = move
            if alpha >= beta:
                break
        return alpha    
    
    return alphabeta(cur_state, 6, player_to_move)

def get_valid_moves(board, turn):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, turn):
                valid_moves.append((row, col))
    return valid_moves

def is_valid_move(board, row, col, turn):
    if board[row][col] != 0:
        return False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            
            r = row + i
            c = col + j
            found_opponent = False
            
            while r >= 0 and r < 8 and c >= 0 and c < 8:
                if board[r][c] == 0:
                    break
                if board[r][c] == turn:
                    if found_opponent:
                        return True
                    break
                found_opponent = True
                r += i
                c += j
    return False

def make_move(board, move, turn):
    row, col = move
    new_board = [row[:] for row in board]
    
    new_board[row][col] = turn
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            
            r = row + i
            c = col + j
            flipped = False
            to_flip = []
            
            while r >= 0 and r < 8 and c >= 0 and c < 8:
                if new_board[r][c] == 0:
                    break
                if new_board[r][c] == turn:
                    flipped = True
                    break
                to_flip.append((r, c))
                r += i
                c += j
            
            if flipped:
                for (r, c) in to_flip:
                    new_board[r][c] = turn
    return new_board

POSITION_SCORES = [[25, 0, 6, 5, 5, 6, 0, 25],
                    [ 0, 0, 1, 1, 1, 1, 0,  0],
                    [ 6, 1, 4, 3, 3, 4, 1,  6],
                    [ 5, 1, 3, 2, 2, 3, 1,  5],
                    [ 5, 1, 3, 2, 2, 3, 1,  5],
                    [ 6, 1, 4, 3, 3, 4, 1,  6],
                    [ 0, 0, 1, 1, 1, 1, 0,  0],
                    [25, 0, 6, 5, 5, 6, 0, 25]]

def heuristic(cur_state, player_to_move):
    score = 0
    for i in range(8):
        for j in range(8):
            score += cur_state[i][j] * POSITION_SCORES[i][j]

    for i in range(8):
        row_pieces = [cur_state[i][0]]
        col_pieces = [cur_state[0][i]]
        for j in range(1,8):
            if row_pieces[-1] * cur_state[i][j] > 0:
                row_pieces[-1] += cur_state[i][j]
            else:
                row_pieces.append(cur_state[i][j])
            
            if col_pieces[-1] * cur_state[j][i] > 0:
                col_pieces[-1] += cur_state[j][i]
            else:
                col_pieces.append(cur_state[j][i])

        if len(row_pieces) >= 3:
            for j in range(1, len(row_pieces)-1):
                if row_pieces[j] != 0:
                    if row_pieces[j-1] * row_pieces[j+1] == 0 and row_pieces[j-1] + row_pieces[j+1] != 0:
                        score -= row_pieces[j] * 1

        if len(col_pieces) >= 3:
            for j in range(1, len(col_pieces)-1):
                if col_pieces[j] != 0:
                    if col_pieces[j-1] * col_pieces[j+1] == 0 and col_pieces[j-1] + col_pieces[j+1] != 0:
                        score -= col_pieces[j] * 1

    if cur_state[0][0] == 0:
        score -= (cur_state[1][0] + cur_state[0][1] + cur_state[1][1])*3
    if cur_state[0][7] == 0:
        score -= (cur_state[1][7] + cur_state[0][6] + cur_state[1][6])*3
    if cur_state[7][0] == 0:
        score -= (cur_state[7][1] + cur_state[6][0] + cur_state[6][1])*3
    if cur_state[7][7] == 0:
        score -= (cur_state[6][7] + cur_state[7][6] + cur_state[6][6])*3
    
    return (score * player_to_move)