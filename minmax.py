import random

def minimax(cur_state, player_to_move, depth, alpha, beta):
    MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
    (0, -1), (0, +1),
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

    if depth == 0 or not get_legal_moves(cur_state, player_to_move):
        return None, evaluate(cur_state, player_to_move)

    if player_to_move == 1:
        max_value = float('-inf')
        best_move = None
        for move in get_legal_moves(cur_state, player_to_move):
            new_state = make_move(cur_state, move, player_to_move)
            _, value = minimax(new_state, -player_to_move, depth - 1, alpha, beta)
            if value > max_value:
                max_value = value
                best_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return best_move, max_value
    else:
        min_value = float('inf')
        best_move = None
        for move in get_legal_moves(cur_state, player_to_move):
            new_state = make_move(cur_state, move, player_to_move)
            _, value = minimax(new_state, -player_to_move, depth - 1, alpha, beta)
            if value < min_value:
                min_value = value
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_move, min_value
def evaluate(board, player_to_move):
    score = 0
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            if tile == player_to_move:
                score += 1
                if i in [0, 7] or j in [0, 7]:
                    score += 2
                if i in [0, 7] and j in [0, 7]:
                    score += 5
                    
            elif tile == -player_to_move:
                score -= 1
                if i in [0, 7] or j in [0, 7]:
                    score -= 2
                if i in [0, 7] and j in [0, 7]:
                    score -= 5
    return score
def get_best_move(cur_state, player_to_move, remain_time=1, depth=5):
    if player_to_move == 1:
        depth = 4
    move, _ = minimax(cur_state, player_to_move, depth, float('-inf'), float('inf'))
    return move