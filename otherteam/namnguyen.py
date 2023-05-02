import numpy as np


# CÁC HÀM CHUNG
def is_valid_position(x, y):
    return x >= 0 and x < 8 and y >= 0 and y < 8


def is_valid_move(board, player, move):
    x, y = move

    if not board[x][y] == 0:
        return False

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for d in directions:
        c, r = x + d[0], y + d[1]

        if is_valid_position(c, r) and board[c][r] == -player:
            c, r = c + d[0], r + d[1]

            while is_valid_position(c, r) and board[c][r] == -player:
                c, r = c + d[0], r + d[1]

            if is_valid_position(c, r) and board[c][r] == player:
                return True

    return False


def make_move(board, player, move):
    x, y = move
    board[x][y] = player

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for d in directions:
        c, r = x + d[0], y + d[1]

        if is_valid_position(c, r) and board[c][r] == -player:
            c, r = c + d[0], r + d[1]

            while is_valid_position(c, r) and board[c][r] == -player:
                c, r = c + d[0], r + d[1]

            if is_valid_position(c, r) and board[c][r] == player:
                c, r = x + d[0], y + d[1]

                while board[c][r] == -player:
                    board[c][r] = player
                    c, r = c + d[0], r + d[1]


def get_valid_move(board, player):
    valid_moves = []
    for x in range(8):
        for y in range(8):
            if is_valid_move(board, player, (x, y)):
                valid_moves.append((x, y))
    return valid_moves


def get_score(board):
    score_dict = {1: 0, -1: 0, 0: 0}
    for x in range(8):
        for y in range(8):
            score_dict[board[x][y]] += 1
    return score_dict


def is_game_over(board):
    score = get_score(board)

    # Trường hợp bàn cờ đã lắp đầy
    if score[1] + score[-1] == 64:
        return True

    # Trường hợp cả hai không có nước đi hợp lệ
    if not get_valid_move(board, 1) and not get_valid_move(board, -1):
        return True

    return False


# CÁC HÀM HEURISTIC
def count_pieces(board, player):
    count = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == player:
                count += 1
    return count


def parity_heuristic(board, player):
    cur_count = count_pieces(board, player)
    opp_count = count_pieces(board, -player)
    return 100 * (cur_count - opp_count) / (cur_count + opp_count)


def count_corners(board, player):
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    count = 0
    for corner in corners:
        if board[corner[0]][corner[1]] == player:
            count += 1
    return count


def corner_heuristic(board, player):
    cur_corners = count_corners(board, player)
    opp_corners = count_corners(board, -player)
    if cur_corners + opp_corners != 0:
        return 100 * (cur_corners - opp_corners) / (cur_corners + opp_corners)
    else:
        return 0


def count_corners_captured(board, player):
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    count = 0
    for corner in corners:
        if board[corner[0]][corner[1]] == player:
            count += 1
        elif board[corner[0]][corner[1]] == -player:
            count -= 1
    return count


def corners_captured_heuristic(board, player):
    cur_corners_captured = count_corners_captured(board, player)
    opp_corners_captured = count_corners_captured(board, -player)
    if cur_corners_captured + opp_corners_captured != 0:
        return (
            100
            * (cur_corners_captured - opp_corners_captured)
            / (cur_corners_captured + opp_corners_captured)
        )
    else:
        return 0


# CÁC HÀM ĐỂ CHỌN NƯỚC ĐI TỐT NHẤT
def combined_heuristic(board, player):
    weights = [0.2, 0.3, 0.2]  # Assign weights to each heuristic
    h1 = parity_heuristic(board, player)
    h2 = corner_heuristic(board, player)
    h3 = corners_captured_heuristic(board, player)
    combined_h = weights[0] * h1 + weights[1] * h2 + weights[2] * h3
    return combined_h


transposition_table = {}


def evaluate(board, player):
    transposition_key = hash(tuple(tuple(row) for row in board))
    if transposition_key in transposition_table:
        return transposition_table[transposition_key]
    score = combined_heuristic(board, player)
    transposition_table[transposition_key] = score
    return score


def negamax(board, player, depth, alpha, beta, killer_moves):
    if depth == 0 or is_game_over(board):
        return evaluate(board, player), None

    best_move = None
    for move in get_valid_move(board, player):
        new_board = np.copy(board)
        make_move(new_board, player, move)

        if move not in killer_moves:
            killer_moves += [move]

        score, _ = negamax(new_board, -player, depth - 1, -beta, -alpha, killer_moves)
        score = -score

        if score > alpha:
            alpha = score
            best_move = move

        if alpha >= beta:
            break

    return alpha, best_move


def select_move(cur_state, player_to_move, remain_time):
    _, best_move = negamax(cur_state, player_to_move, 5, -np.inf, np.inf, [])
    return best_move