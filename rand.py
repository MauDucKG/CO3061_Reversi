import random


def rand(cur_state, player_to_move, remain_time=1):
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

    def is_valid_coord(row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_legal_move(board, move, player_to_move):
        return move != () and is_valid_coord(move[0], move[1]) and board[move[0]][move[1]] == 0 and any(has_tile_to_flip(board, move, direction, player_to_move) for direction in MOVE_DIRS)

    def get_legal_moves(cur_state, player_to_move):
        return [(row, col) for row in range(8) for col in range(8) if is_legal_move(cur_state, (row, col), player_to_move)]

    moves = get_legal_moves(cur_state, player_to_move)
    if moves:
        return random.choice(moves)
    else:
        return None
