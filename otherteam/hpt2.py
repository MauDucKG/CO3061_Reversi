import time
import copy
import random

	
def findValidDirections(x, y):
	validDirections = []

	if y != 0: validDirections.append("UP")
	if y != 0 and x != 0: validDirections.append("UP_LEFT")
	if y != 0 and x != 7: validDirections.append("UP_RIGHT")

	if y != 7: validDirections.append("DOWN")
	if y != 7 and x != 0: validDirections.append("DOWN_LEFT")
	if y != 7 and x != 7: validDirections.append("DOWN_RIGHT")

	if x != 0: validDirections.append("LEFT")
	if x != 7: validDirections.append("RIGHT")

	return validDirections

def checkUP(x, y, state, currentPlayer):
	if state[y][x] == currentPlayer or state[y][x] == 0: return False
	y -= 1
	while y >= 0 :
		if state[y][x] == 0: return False
		if state[y][x] == currentPlayer: return True
		y -= 1
	
	return False

def checkDOWN(x, y, state, currentPlayer):
	if state[y][x] == currentPlayer or state[y][x] == 0: return False
	y += 1
	while y <= 7 :
		if state[y][x] == 0: return False
		if state[y][x] == currentPlayer: return True
		y += 1
	
	return False

def checkLEFT(x, y, state, currentPlayer):

	if state[y][x] == currentPlayer or state[y][x] == 0: return False
	x -= 1
	while x >= 0 :
		if state[y][x] == 0: return False
		if state[y][x] == currentPlayer: return True
		x -= 1
	
	return False

def checkRIGHT(x, y, state, currentPlayer):
	if state[y][x] == currentPlayer or state[y][x] == 0: return False
	x += 1
	while x <= 7 :
		if state[y][x] == 0: return False
		if state[y][x] == currentPlayer: return True
		x += 1
	
	return False

def checkUP_LEFT(x, y, state, currentPlayer):
	if state[y][x] == currentPlayer or state[y][x] == 0: return False
	x -= 1
	y -= 1
	while x >= 0 and y >= 0 :
		if state[y][x] == 0: return False
		if state[y][x] == currentPlayer: return True
		x -= 1
		y -= 1
	
	return False

def checkUP_RIGHT(x, y, state, currentPlayer):
	if state[y][x] == currentPlayer or state[y][x] == 0: return False
	x += 1
	y -= 1
	while x <= 7 and y >= 0 :
		if state[y][x] == 0: return False
		if state[y][x] == currentPlayer: return True
		x += 1
		y -= 1
	
	return False

def checkDOWN_RIGHT(x, y, state, currentPlayer):
	if state[y][x] == currentPlayer or state[y][x] == 0: return False
	x += 1
	y += 1
	while x <= 7 and y <= 7 :
		if state[y][x] == 0: return False
		if state[y][x] == currentPlayer: return True
		x += 1
		y += 1
	
	return False

def checkDOWN_LEFT(x, y, state, currentPlayer):
	if state[y][x] == currentPlayer or state[y][x] == 0: return False
	x -= 1
	y +=1
	while x >= 0 and y <= 7 :
		if state[y][x] == 0: return False
		if state[y][x] == currentPlayer: return True
		x -= 1
		y += 1
	
	return False

def searchUP(state, x, y, currentPlayer):
	if state[y][x] == 0 or state[y][x] == currentPlayer:
		return state
	oldstate = copy.deepcopy(state)

	while y >= 0:
		if state[y][x] == 0: return oldstate
		if state[y][x] == currentPlayer:
			return state
		state[y][x] = currentPlayer
		y -= 1
	return oldstate

def searchDOWN(state,x, y, currentPlayer):
	if state[y][x] == 0 or state[y][x] == currentPlayer:
		return state
	oldstate = copy.deepcopy(state)

	while y <= 7:
		if state[y][x] == 0: return oldstate
		if state[y][x] == currentPlayer:
			return state
		state[y][x] = currentPlayer
		y += 1
	return oldstate

def searchLEFT(state, x, y, currentPlayer):
	if state[y][x] == 0 or state[y][x] == currentPlayer:
		return state
	oldstate = copy.deepcopy(state)

	while x >= 0:
		if state[y][x] == 0: return oldstate
		if state[y][x] == currentPlayer:
			return state
		state[y][x] = currentPlayer
		x -= 1
	return oldstate

def searchRIGHT(state, x, y, currentPlayer):
	if state[y][x] == 0 or state[y][x] == currentPlayer:
		return state
	oldstate = copy.deepcopy(state)

	while x <= 7:
		if state[y][x] == 0: return oldstate
		if state[y][x] == currentPlayer:
			return state
		state[y][x] = currentPlayer
		x += 1
	return oldstate

def searchUP_LEFT(state, x, y, currentPlayer):
	if state[y][x] == 0 or state[y][x] == currentPlayer:
		return state
	oldstate = copy.deepcopy(state)

	while x >= 0 and y >= 0:
		if state[y][x] == 0: return oldstate
		if state[y][x] == currentPlayer:
			return state
		state[y][x] = currentPlayer
		x -= 1
		y -= 1
	return oldstate

def searchDOWN_LEFT(state, x, y, currentPlayer):
	if state[y][x] == 0 or state[y][x] == currentPlayer:
		return state
	oldstate = copy.deepcopy(state)

	while x >= 0 and y <= 7:
		if state[y][x] == 0: return oldstate
		if state[y][x] == currentPlayer:
			return state
		state[y][x] = currentPlayer
		x -= 1
		y += 1
	return oldstate

def searchUP_RIGHT(state, x, y, currentPlayer):
	if state[y][x] == 0 or state[y][x] == currentPlayer:
		return state
	oldstate = copy.deepcopy(state)

	while x <= 7 and y >= 0:
		if state[y][x] == 0: return oldstate
		if state[y][x] == currentPlayer:
			return state
		state[y][x] = currentPlayer
		x += 1
		y -= 1
	return oldstate

def searchDOWN_RIGHT(state, x, y, currentPlayer):
	if state[y][x] == 0 or state[y][x] == currentPlayer:
		return state
	oldstate = copy.deepcopy(state)

	while x <= 7 and y <= 7:
		if state[y][x] == 0: return oldstate
		if state[y][x] == currentPlayer:
			return state
		state[y][x] = currentPlayer
		x += 1
		y += 1
	return oldstate

def findValidMove(state, currentPlayer):
		validMove = []
		for y in range(8):
			for x in range(8):

				if state[y][x] != 0:
					continue
			
				validDirections = findValidDirections(x,y)

				for direction in validDirections:

					
					if direction == "UP":
						if checkUP(x, y-1, state, currentPlayer):
							validMove.append((x, y))
							break

					if direction == "DOWN":
						if checkDOWN(x, y+1, state, currentPlayer):
							validMove.append((x, y))
							break

					if direction == "LEFT":
						if checkLEFT(x-1, y, state, currentPlayer):
							validMove.append((x, y))
							break
					
					if direction == "RIGHT":
						if checkRIGHT(x+1, y, state, currentPlayer):
							validMove.append((x, y))
							break

					if direction == "UP_LEFT":
						if checkUP_LEFT(x-1, y-1, state, currentPlayer):
							validMove.append((x, y))
							break

					if direction == "UP_RIGHT":
						if checkUP_RIGHT(x+1, y-1, state, currentPlayer):
							validMove.append((x, y))
							break

					if direction == "DOWN_LEFT":
						if checkDOWN_LEFT(x-1, y+1, state, currentPlayer):
							validMove.append((x, y))
							break

					if direction == "DOWN_RIGHT":
						if checkDOWN_RIGHT(x+1, y+1, state, currentPlayer):
							validMove.append((x, y))
							break

		return validMove
	
def makeMove(state, Cell, currentPlayer):
			x, y = Cell
			state[y][x] = currentPlayer
			if y > 1: state = searchUP(state, x, y-1, currentPlayer)
			if y < 6: state = searchDOWN(state, x, y+1, currentPlayer)
			if x > 1: state = searchLEFT(state, x-1, y, currentPlayer)
			if x < 6: state = searchRIGHT(state, x+1, y,currentPlayer)
			if x > 1 and y > 1: state = searchUP_LEFT(state, x-1, y-1, currentPlayer)
			if x > 1 and y < 6: state = searchDOWN_LEFT(state, x-1, y+1, currentPlayer)
			if x < 6 and y > 1: state = searchUP_RIGHT(state, x+1, y-1, currentPlayer)
			if x < 6 and y < 6: state = searchDOWN_RIGHT(state, x+1, y+1, currentPlayer)
			return state

def isGoodCellNextToCorner(state, player, Cell):
	#UP LEFT CORNER
	if state[0][0] == player:
		if Cell in [(0,1), (1,0)]: return True
		if Cell == (1,1) and state[1][0] ==  state[0][1] == state[0][2] == player == state[2][0] == player: return True
	
	#UP RIGHT CORNER
	if state[0][7] == player:
		if Cell in [(6,0), (7,1)]: return True
		if Cell == (6,1) and state[0][6] == state[1][7] == state[0][5] == state[2][7] == player: return True

	#BOTTOM LEFT CORNER
	if state[7][0] == player:
		if Cell in [(0,6), (1,7)]: return True
		if Cell == (1,6) and state[6][0] == state[7][1] == state[5][0] == state[7][2] == player: return True


	#BOTTOM RIGHT CORNER
	if state[7][7] == player:
		if Cell in [(6,7), (7,6)]: return True
		if Cell == (6,6) and state[7][6] == state[6][7] == state[7][5] == state[5][7] == player: return True
	
	"""Good if next to corner and around is all opponent"""
	if Cell == (1,1) and state[0][0] == state[1][0] == state[0][1] == state[0][2] == state[2][0] == state[2][2]\
		== state[1][2] == state[2][1] == -player: return True
	
	if Cell == (6,1) and state[0][6] == state[1][7] == state[0][5] == state[2][7] \
		== state[0][7] == state[2][5] == state[5][1] == state[2][6] == -player: return True
	
	if Cell == (1,6) and state[6][0] == state[7][1] == state[5][0] == state[7][2]\
		== state[7][0] == state[5][1] == state[5][2] == state[6][2] == -player: return True
	
	if Cell == (6,6) and state[7][6] == state[6][7] == state[7][5] == state[5][7]\
		 == state[7][7] == state[5][5] == state[5][6] == state[6][5] == player: return True

	#Cell next to corner is bad
	return False

def isNextToCorner(Cell):
	if Cell in [(0,1), (1,0), (1,1), (6,0), (7,1), (6,1), (0,6), (1,7), (1,6), (6,7), (7,6), (6,6)]:
		return True
	return False

def select_move(cur_state, player_to_move, remain_time):
	start = time.perf_counter()
	validMove = findValidMove(cur_state, player_to_move)
	state = copy.deepcopy(cur_state)
	#print(validMove)
	
	if validMove == []:
		return None

	if (0,0) in validMove: return (0,0)
	if (0,7) in validMove: return (0,7)
	if (7,0) in validMove: return (7,0)
	if (7,7) in validMove: return (7,7)


	move = minimax_alpha_beta(state, player_to_move, validMove, 0, start, remain_time, -64, 64)

	return move[1] if move and move[1] else random.choice(validMove)


def minimax_alpha_beta(cur_state, player_to_move, validMove, depth,start, remain_time, alpha, beta):

	execution_time = time.perf_counter() - start
	if execution_time > 2.995 or remain_time -  execution_time  <= 0.0005:
		#print(execution_time)
		return None
	
	best_move = None
	if depth == 10 or validMove == []:
		#print(player_to_move)
		return evaluate(cur_state, player_to_move), None

	
	for a_move in validMove:
		
		if a_move in [(0,0), (0,7), (7,0), (7,7)]:
			#return evaluate(cur_state, player_to_move) +18, None
			return 64, None

		if isNextToCorner(a_move):
			if isGoodCellNextToCorner(cur_state, player_to_move, a_move):
				return 64, a_move
			new_val = -64

		else:
			state = makeMove(cur_state, a_move, player_to_move)
			new_valid_move = findValidMove(state, -player_to_move)
			res = minimax_alpha_beta(state, -player_to_move, new_valid_move, depth+1, start, remain_time, -beta, -alpha)
			if res == None:	
				return None
			new_val = -res[0]

		if new_val > alpha:
			alpha = new_val
			best_move = a_move

		
		if alpha >= beta:
			return alpha, best_move

	#print (best_move)
	return -64, best_move

def evaluate(state, player_to_move):
	score = 0
	for y in range(8):
		for x in range(8):
			if state[y][x] == player_to_move:
				score += 1
			#if state[y][x] == -player_to_move:
			#	score -= 1
	return score - len(findValidMove(state, -player_to_move))