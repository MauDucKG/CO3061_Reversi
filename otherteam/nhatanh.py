import sys
import time
import random
from copy import deepcopy

class Board:
  def __init__(self):
    # board[row][col] in UI
    self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, -1, 0, 0, 0],
                  [0, 0, 0, -1, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]
    self.heuristic = [[1000, -10, 5, 5, 5, 5, -10, 1000],
                  [-10, -20, -1, -1, -1, -1, -20, -10],
                  [5, -1, 1, 1, 1, 1, -1, 5],
                  [5, -1, 1, 1, 1, 1, -1, 5],
                  [5, -1, 1, 1, 1, 1, -1, 5],
                  [5, -1, 1, 1, 1, 1, -1, 5],
                  [-10, -20, -1, -1, -1, -1, -20, -10],
                  [1000, -20, 10, 10, 10, 10, -20, 1000]]
    self.possible_move = []
    self.direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
  def update_board(self, cur_state):
    self.board = deepcopy(cur_state)
    return self.board
  def current_board(self):
    return self.board
  
  def count(self):
    count_X = 0
    count_O = 0
    for i in range(8):
      for j in range(8):
        if self.board[i][j] == -1:
          count_X += 1
        elif self.board[i][j] == 1:
          count_O += 1
    return count_X, count_O
  def weighted_score(self, player_to_move):
    other = - player_to_move
    total = 0
    for i in range(8):
      for j in range(8):
        if self.board[i][j] == player_to_move:
          total += self.heuristic[i][j]
        elif self.board[i][j] == other:
          total -= self.heuristic[i][j]
    return total

  def check_direction(self, row, col, row_add, col_add, other):
    i = row + row_add
    j = col + col_add
    # check neighbor: other color -> valid move
    if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other):
      i += row_add
      j += col_add
      while (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == other):
        i += row_add
        j += col_add
      if (i >= 0 and j >= 0 and i < 8 and j < 8 and self.board[i][j] == 0):
        return (i, j)
  
  #lookup
  def is_possible_move(self, row, col, player):
    if player == -1:
      other = 1
    else: other = -1
    
    is_possible_move = []
    
    for (x, y) in self.direction: # 8 direction
      pos = self.check_direction(row, col, x, y, other) # return posible (x, y)
      if pos: 
        is_possible_move.append(pos)
    return is_possible_move

  #get_valid_move
  def check_possible_moves(self, player):
    if player == -1:
      other = 1
    else: other = -1

    possible_move = []
    for i in range(8):
      for j in range(8):
        if self.board[i][j] == player:
          possible_move = possible_move + self.is_possible_move(i, j, player)
    possible_move = list(set(possible_move))
    self.possible_move = possible_move
    return possible_move

  def flip(self, position, x, y, player): # (x, y) is direction of move
    flip_square = []
    i = position[0] + x
    j = position[1] + y
    
    if player == -1:
      other = 1
    else: other = -1
    if i in range(8) and j in range(8) and self.board[i][j] == other:
      flip_square = flip_square + [(i, j)]
      i = i + x
      j = j + y
    while i in range(8) and j in range(8) and self.board[i][j] == other:
      flip_square = flip_square + [(i, j)]
      i = i + x
      j = j + y
    # print(flip_square)
    if i in range(8) and j in range(8) and self.board[i][j] == player:
      for square in flip_square:
        self.board[square[0]][square[1]] = player
      
  def apply_move(self, move, player):
    self.possible_move = self.check_possible_moves(player)
    if move in self.possible_move:
      self.board[move[0]][move[1]] = player
      for (x, y) in self.direction:
        self.flip(move, x, y, player)
    
    # for i in self.board:
    #   print(i)
    
  # ------ Minimax ------
def minimax_max_node(cur_state, player_to_move, depth, remain_time):
	best_max_score = -9999999
	other = -player_to_move
	cur_board = Board()
	board = cur_board.update_board(cur_state)
	possible_move = cur_board.check_possible_moves(player_to_move)
    
	if possible_move == [] or depth == 0:
		score = cur_board.weighted_score(other)
		# print(score)
		return score
	else:
		for move in possible_move:
			new_board = Board()
			new_board.update_board(cur_state)
			new_board.apply_move(move, player_to_move)
			created_board = new_board.current_board()
			move_score = minimax_min_node(created_board, other, depth-1, remain_time)
			if move_score > best_max_score:
				best_max_score = move_score
	return best_max_score
    
def minimax_min_node(cur_state, player_to_move, depth, remain_time):
	best_min_score = 9999999
	other = -player_to_move
	cur_board = Board()
	board = cur_board.update_board(cur_state)
	possible_move = cur_board.check_possible_moves(player_to_move)
    
	if possible_move == [] or depth == 0:
		score = cur_board.weighted_score(other)
		# print(score)
		return score
	else:
		for move in possible_move:
			new_board = Board()
			new_board.update_board(cur_state)
			new_board.apply_move(move, player_to_move)
			created_board = new_board.current_board()
			move_score = minimax_max_node(created_board, other, depth-1, remain_time)
			if move_score < best_min_score:
				best_min_score = move_score
	return best_min_score
def minimax(cur_state, player_to_move, depth, remain_time):
	best_max_score = -9999999
	best_move = None
	other = -player_to_move
	cur_board = Board()
	board = cur_board.update_board(cur_state)
	possible_move = cur_board.check_possible_moves(player_to_move)

	for move in possible_move:
		new_board = Board()
		new_board.update_board(cur_state)
		new_board.apply_move(move, player_to_move)
		created_board = new_board.current_board()

		move_score = minimax_min_node(created_board, other, depth-1, remain_time)
		if move_score > best_max_score:
			best_max_score = move_score
			best_move = move

	print('Best move: ', best_move)
	return best_move
  # ------ Minimax ------

def select_move(cur_state, player_to_move, remain_time):
	NewBoard = Board()
	NewBoard.update_board(cur_state)
	start_time = time.time()
	depth = 3
	
	possible_move = NewBoard.check_possible_moves(player_to_move)
	if possible_move:
		random_move = random.choice(possible_move)
		minimax_move = minimax(cur_state, player_to_move, depth, remain_time)

		end_time = time.time()
		computer_time = round(end_time - start_time, 2)
		remain_time -= computer_time
		if computer_time > 3:
			print('Computer: Time out!!!', computer_time)
		# return random_move
		return minimax_move
	else: 
		print('Computer: Out of moves!')
	return None

